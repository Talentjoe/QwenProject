import json
import functionDefineAndDiscription
import re

from transformers import AutoModelForCausalLM, AutoTokenizer


class genCall:
    DEBUG = True

    def __init__(self,modelNmae):
        model_name = modelNmae

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.tools = functionDefineAndDiscription.TOOLS
        self.messages = functionDefineAndDiscription.MESSAGES[:]

    def printLLMAOutputWithFunctionCall(self, outputString: str):
        if not self.DEBUG:
            outputString = re.sub(r"<tool_call>\n(.+)?\n</tool_call>", "Function Called\n", outputString)
            outputString = re.sub(r"<\|im_end\|>", "\n End generation", outputString)
        print(outputString)

    def try_parse_tool_calls(self,content: str):
        """Try parse the tool calls."""
        tool_calls = []
        offset = 0
        for i, m in enumerate(re.finditer(r"<tool_call>\n(.+)?\n</tool_call>", content)):
            if i == 0:
                offset = m.start()
            try:
                func = json.loads(m.group(1))
                tool_calls.append({"type": "function", "function": func})
                if isinstance(func["arguments"], str):
                    func["arguments"] = json.loads(func["arguments"])
            except json.JSONDecodeError as e:
                print(f"Failed to parse tool calls: the content is {m.group(1)} and {e}")
                pass
        if tool_calls:
            if offset > 0 and content[:offset].strip():
                c = content[:offset]
            else:
                c = ""
            return [{"role": "assistant", "content": c, "tool_calls": tool_calls}, True]
        return [{"role": "assistant", "content": re.sub(r"<\|im_end\|>$", "", content)}, False]

    def generateText(self, userInput: str, ifPrint: bool = False, maxToken: int = 512):

        returnText = ""

        self.messages.append({"role": "user", "content": userInput})
        text = self.tokenizer.apply_chat_template(self.messages, tools=self.tools, add_generation_prompt=True, tokenize=False)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=maxToken)
        output_text = self.tokenizer.batch_decode(outputs)[0][len(text):]

        returnText += output_text
        if (ifPrint):
            self.printLLMAOutputWithFunctionCall(output_text)

        while True:
            parse_result = self.try_parse_tool_calls(output_text)
            self.messages.append(parse_result[0])

            if (not parse_result[1]):
                break

            if tool_calls := self.messages[-1].get("tool_calls", None):
                for tool_call in tool_calls:
                    if fn_call := tool_call.get("function"):
                        fn_name: str = fn_call["name"]
                        fn_args: dict = fn_call["arguments"]

                        fn_res: str = json.dumps(functionDefineAndDiscription.get_function_by_name(fn_name)(**fn_args))

                        self.messages.append({
                            "role": "tool",
                            "name": fn_name,
                            "content": fn_res,
                        })

            # print(messages)

            text = self.tokenizer.apply_chat_template(self.messages, tools=self.tools, add_generation_prompt=True, tokenize=False)
            inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(**inputs, max_new_tokens=maxToken)
            output_text = self.tokenizer.batch_decode(outputs)[0][len(text):]

            if (ifPrint):
                self.printLLMAOutputWithFunctionCall(output_text)
            returnText += output_text

            self.messages.append(self.try_parse_tool_calls(output_text)[0])

            return returnText

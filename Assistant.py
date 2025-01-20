import time
from datetime import datetime
from time import strftime
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,StoppingCriteriaList,StoppingCriteria
from transformers import TextStreamer

device = "cuda" # the device to load the model onto
name = "Qwen/Qwen2.5-3B-Instruct"
messages = ([
        {"role": "system", "content": "You are a helpful assistant."},
    ])


# Now you do not need to add "trust_remote_code=True"
model = AutoModelForCausalLM.from_pretrained(
    name,
    torch_dtype="auto",
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(name)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token if missing
    tokenizer.pad_token_id = tokenizer.eos_token_id + 1  # Assign a unique ID for padding

while True:
    # Instead of using model.chat(), we directly use model.generate()
    # But you need to use tokenizer.apply_chat_template() to format your inputs as shown below
    prompt = input("You: ")
    if prompt == "bye":
        break
    messages.append({"role": "user", "content": prompt})

    print(messages)

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    # Directly use generate() and tokenizer.decode() to get the output.
    # Use `max_new_tokens` to control the maximum output length.
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)


    print("Qwen: ",end="" )
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512,
        streamer=streamer,
    )
    #print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
    messages.append({"role": "Qwen", "content": tokenizer.decode(generated_ids[0], skip_special_tokens=True).split("assistant")[-1]})
    print("----end----")

path = r"ChatHistory\chat_history_"+strftime("%Y-%m-%d_%H-%M-%S")
with open(path+ ".txt", "w", encoding='utf-8') as f:
    for message in messages:
        f.write(f"{message['role']}: {message['content']}\n")
with open(path + ".json", "w", encoding='utf-8') as f:
    json.dump(messages, f, ensure_ascii=False, indent=4)
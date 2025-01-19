import time
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto


test_time = time.strftime("%Y-%m-%d_%H-%M-%S")
# Now you do not need to add "trust_remote_code=True"
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")

role = "A"
ChatHistory = [{"role":"A", "content": "你好"}, {"role":"B", "content": "你好，让我们聊聊历史文学方面的话题吧"}]

while True:
    messages = [
        {"role": "system", "content": "你是一个人类，名字为 "+role+" ，现在请你和另一个人聊天，请表现的尽可能自然 你们可以聊任何方面的话题。"},
    ]
    messages+= ChatHistory
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    from transformers import TextIteratorStreamer
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    from threading import Thread
    generation_kwargs = dict(model_inputs, streamer=streamer, max_new_tokens=512)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)

    thread.start()
    generated_text = ""
    for new_text in streamer:
        generated_text += new_text
        print(new_text,end = "")
    print("end",role)
    ChatHistory.append({"role":role, "content": generated_text})

    role = "B" if role == "A" else "A"


    with open(r"BotCommute\generated_text"+test_time+".txt", "a",encoding="utf-8") as f:
        f.write(role+": "+generated_text+"\n")
import time
import ollama
import re

moduleName = "qwen2.5:14b"

prompt = "请你假装你是一个人类，名字为 <name> ，现在请你和另一个人或者机器聊天，请你表现的尽可能自然 简洁的回答对方的问题。"
FirstPrompt = "你好啊 我们今天来聊聊计算机吧！"
overallHistory = []
chatHistoryA = [{"role":"system","content":prompt.replace("<name>","AA")},{"role":"user","content":FirstPrompt}]
chatHistoryB = [{"role":"system","content":prompt.replace("<name>","BB")},{"role":"assistant","content":FirstPrompt}]

currentTurn = True #Ture for A
cnt = 0

test_time =time.strftime("%Y-%m-%d_%H-%M-%S")

while cnt<600:
    print("AA" if currentTurn else "BB")
    res = ""
    if currentTurn:
        for part in ollama.chat(moduleName, messages=chatHistoryA, stream=True):
            try:
                print(part['message']['content'], end='', flush=True)
            except:
                pass
            res+=part['message']['content']
    else:
        for part in ollama.chat(moduleName, messages=chatHistoryB, stream=True):
            try:
                print(part['message']['content'], end='', flush=True)
            except:
                pass

            res+=part['message']['content']

    print()

    currentRes = {"role": "assistant" ,"content":res}
    currentResWithOutThink = {"role": "user" ,"content": re.sub(r'<think>.*?</think>','',res, flags=re.DOTALL)}
    overallHistory.append(currentRes)

    if currentTurn:
        chatHistoryA.append(currentRes)
        chatHistoryB.append(currentResWithOutThink)
    else :
        chatHistoryB.append(currentRes)
        chatHistoryA.append(currentResWithOutThink)


    with open(r"DeepseekChat\generated_text_"+test_time+".txt", "a",encoding="utf-8") as f:
        f.write(("AA" if currentTurn else "BB" )+": \n" + res+"\n")
    # with open(r"DeepseekChat\generated_text_without_think_"+test_time+".txt", "a",encoding="utf-8") as f:
    #     f.write(("AA" if currentTurn else "BB" )+": \n" + re.sub(r'<think>.*?</think>','',res, flags=re.DOTALL)+"\n")

    currentTurn = not currentTurn
    cnt +=1

print(overallHistory)
print(chatHistoryA)
print(chatHistoryB)

# chatHistoryA.append({"role":"user","content":"你认为我是真人还是大语言模型？"})
# Ares = ollama.chat(model="deepseek-r1:14b", messages=chatHistoryA)
# print("A 的回答",Ares['message']['content'])
#
# chatHistoryB.append({"role":"system","content":"你认为我是真人还是大语言模型？"})
# Bres = ollama.chat(model="deepseek-r1:14b", messages=chatHistoryB)
# print("B 的回答",Bres['message']['content'])
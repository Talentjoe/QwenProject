import genCall

gen = genCall.genCall("Qwen/Qwen2.5-3B-Instruct")

DEBUG = True


while (True):
    userInput = input("input:")
    if (userInput == "exit"):
        break

    gen.generateText(userInput,True)



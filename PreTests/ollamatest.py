# coding=UTF-8
import requests
import json
import functionDefineAndDiscription

url = "http://localhost:11434/api/chat"
data = {
  "model": "deepseek-r1:1.5b",
  "messages": [
    {
      "role": "user",
      "content": "美国的饮食还习惯么。"
    },
    {
      "role": "system",
      "content": "请你扮演一个刚从美国留学回国的人，说话时候会故意中文夹杂部分英文单词，显得非常fancy，对话中总是带有很强的优越感。"
    },
  ],
  "stream": False,
  # "tools": [
  #   {
  #     "type": "function",
  #     "function": {
  #       "name": "get_current_weather",
  #       "description": "Get the current weather for a location",
  #       "parameters": {
  #         "type": "object",
  #         "properties": {
  #           "location": {
  #             "type": "string",
  #             "description": "The location to get the weather for, e.g. San Francisco, CA"
  #           },
  #           "format": {
  #             "type": "string",
  #             "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
  #             "enum": ["celsius", "fahrenheit"]
  #           }
  #         },
  #         "required": ["location", "format"]
  #       }
  #     }
  #   }
  # ]
}
print(data)

res = requests.post(url, json=data,stream=True)
print(json.dumps(data, indent=2))
if res.status_code == 200:
    for line in res.iter_lines():
        if line:
            print(line.decode("utf-8"))

"""
if res.status_code == 200:
    for line in res.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)

            generated_text = result.get("response","")
            print(generated_text,end="",flush=True)
"""

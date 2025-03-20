# from openai import OpenAI

# client = OpenAI()

# print(client.models.list())

# --------------------------------

# import os

# from groq import Groq

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# chat_completion = client.models.list()

# print(chat_completion)

# --------------------------------

# import anthropic

# client = anthropic.Anthropic()

# print(client.models.list(limit=20))

# --------------------------------

# import os
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# print("List of models that support generateContent:\n")
# for m in client.models.list():
#     for action in m.supported_actions:
#         if action == "generateContent":
#             print(m.name)

# print("List of models that support embedContent:\n")
# for m in client.models.list():
#     for action in m.supported_actions:
#         if action == "embedContent":
#             print(m.name)

# -------------------------------- deepseek

# from openai import OpenAI

# # for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
# client = OpenAI(api_key="<your API key>", base_url="https://api.deepseek.com")
# print(client.models.list())

# -------------------------------- ollama

# import ollama

# print(ollama.list())

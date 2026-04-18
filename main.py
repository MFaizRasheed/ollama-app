from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='minimax-m2.7:cloud', messages=[
  {
    'role': 'user',
    'content': 'What is machine learning explain in simple words?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)
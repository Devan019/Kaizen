from .client import GroqClient
from const.prompt_template import SPEECH_AI_PROMPT

client = GroqClient().client


#call llm
def get_groq_response(input:str):
  res = client.chat.completions.create(
    model= "openai/gpt-oss-20b",
    messages=[
      {
        "role" : "system",
        "content" : SPEECH_AI_PROMPT
      },
      {
        "role" : "user",
        "content" : input
      }
    ]
  )

  #return res
  return res.choices[0].message.content
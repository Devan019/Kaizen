from .client import GroqClient
from const.prompt_template import SPEECH_AI_PROMPT, SPEECH_TOOL_PROMPT
from tools.tools import TOOLS_SCHEMA, TOOL_MAP
import json

client = GroqClient().client




#call llm
def get_groq_response(messages: list):
  return client.chat.completions.create(
    model= "openai/gpt-oss-20b",
    messages=messages,
    tools=TOOLS_SCHEMA,
    tool_choice="auto"
  )



def run_agent(user_input: str):
    messages = [
        {"role": "system", "content": SPEECH_TOOL_PROMPT},
        {"role": "user", "content": user_input}
    ]

    # First LLM call
    response = get_groq_response(messages)
    msg = response.choices[0].message

    # Check tool call
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]

        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Execute tool
        tool_fn = TOOL_MAP.get(tool_name)
        result = tool_fn(**args)

        # Second LLM call
        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        final_response = get_groq_response(messages)
        return final_response.choices[0].message.content


    # if not tool direct response
    return msg.content

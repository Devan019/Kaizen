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

    MAX_TRIES = 5

    for _ in range(MAX_TRIES):

        # Get LLM response
        response = get_groq_response(messages)
        msg = response.choices[0].message

        # If no tool, final answer
        if not msg.tool_calls:
            return msg.content

        # Add assistant message
        messages.append(msg)

        # Execute all tool calls
        for tool in msg.tool_calls:

            tool_name = tool.function.name
            args = json.loads(tool.function.arguments)

            tool_fn = TOOL_MAP.get(tool_name)

            if not tool_fn:
                result = {"error": f"Tool {tool_name} not found"}
            else:
                result = tool_fn(**args)

            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool.id,
                "content": json.dumps(result)
            })


    return "Max iterations reached"


print(run_agent("can u send a song link of  to my dad"))
import json
import os
from dotenv import load_dotenv
from tools import available_tools
from prompt import SYSTEM_PROMPT
from openai import OpenAI

load_dotenv()

if 'VIRTUAL_ENV' in os.environ:
    print("✅ Inside virtual environment")
else:
    print("⚠️ Not in a virtual environment")

client = OpenAI(api_key=os.getenv("API_KEY_OPENAI"))

messages = [
    { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("> ")
    messages.append({ "role": "user", "content": query })

    done = False

    while not done:
        response = client.chat.completions.create(
            model="gpt-4.1",   
            response_format={"type": "json_object"},
            messages=messages
        )

        reply = response.choices[0].message.content
        messages.append({ "role": "assistant", "content": reply })

        try:
            parsed = json.loads(reply)
        except json.JSONDecodeError:
            print("❌ JSON parse error. Raw response:", reply)
            break

        step = parsed.get("step")

        if step == "plan":
            print("🧠", parsed.get("content"))

        elif step == "action":
            func = parsed.get("function")
            tool_input = parsed.get("input")
            print(f"🛠️ Calling {func}")


            if func in available_tools:
                try:
                    result = available_tools[func](tool_input)
                    obs = json.dumps({ "step": "observe", "output": result })
                    messages.append({ "role": "user", "content": obs })
                except Exception as e:
                    print(f"❌ Tool '{func}' failed:", e)
                    done = True
            else:
                print(f"❌ Unknown tool: {func}")
                done = True
        elif step == "observe":
            print("👀", parsed.get("output"))
        elif step == "followup":
            print("👉", parsed.get("content"))
            user_reply = input("> ")
            messages.append({ "role": "user", "content": user_reply })
        elif step == "complete":
            print("✅", parsed.get("content"))
            done = True
            break  

        # Fallback: If step is a tool name, treat as action
        elif step in available_tools:
            func = step
            tool_input = parsed.get("input")
            print(f"🛠️ (Fallback) Calling {func}({tool_input})")
            try:
                result = available_tools[func](tool_input)
                obs = json.dumps({ "step": "observe", "output": result })
                messages.append({ "role": "user", "content": obs })
            except Exception as e:
                print(f"❌ Tool '{func}' failed:", e)
                done = True

        else:
            print("❓ Unknown step:", step)
            done = True

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from Backend/ regardless of where the script is run from
_env_path = Path(__file__).parent / "Backend" / ".env"
load_dotenv(dotenv_path=_env_path)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def ask_model(messages):
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=messages,
        temperature=0.4,
        top_p=0.9,
        max_tokens=500,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": False},
            "reasoning_budget": 0
        },
        stream=False
    )

    content = completion.choices[0].message.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        final_text = ""
        for block in content:
            if isinstance(block, dict):
                if "text" in block:
                    final_text += block["text"]
                elif "content" in block:
                    final_text += block["content"]
        return final_text.strip()

    return str(content).strip()

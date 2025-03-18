from typing import List
import chainlit as cl
from ctransformers import AutoModelForCausalLM
def get_prompt(instruction: str = '', history: List[str] = []) -> str:
    system = "You are an AI Assistant that gives helpful answers. Your answers should be short and concise."
    prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"
    if history is not None and len(history) > 0:
      prompt += f"This is the conversation history: {''.join(history)}. Now answer the question: "
    prompt += f"${instruction}\n\n### Response:\n"
    return prompt
@cl.on_message
async def on_message(msg: cl.Message):
  message_history = cl.user_session.get("message_history")
  bot_msg = cl.Message(content="")
  await bot_msg.send()
  prompt=get_prompt(msg.content,message_history)
  response=""
  for w in llm(prompt, stream=True):
    await bot_msg.stream_token(w)
    response += w
  await bot_msg.update()
  message_history.append(response)
  cl.Message(llm(get_prompt(msg.content))).send()
@cl.on_chat_start
async def on_chat_start():
  global llm
  llm = AutoModelForCausalLM.from_pretrained(
    'zoltanctoth/orca_mini_3B-GGUF',
    model_file='orca-mini-3b.q4_0.gguf'
	)
  cl.user_session.set("message_history", [])
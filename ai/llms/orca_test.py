from ctransformers import AutoModelForCausalLM
def get_prompt(instruction: str) -> str:
    system = "You are an AI Assistant that gives helpful answers. Your answers should be short and concise."
    return f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"
llm = AutoModelForCausalLM.from_pretrained(
    'zoltanctoth/orca_mini_3B-GGUF',
    model_file='orca-mini-3b.q4_0.gguf'
)
user_input = "Hi! What is your dog's name?"
prompt = get_prompt(user_input)
response = llm(prompt)
print("Full response:", response)
print("Streaming response:")
for w in llm(prompt, stream=True):
    print(w, end="", flush=True)
print()
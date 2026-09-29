with open('integrations/llm.py', 'r', encoding='utf-8') as f:
    llm_code = f.read()

llm_code = llm_code.replace('meta-llama/llama-3.1-8b-instruct:free', 'qwen/qwen3.8-27b:free')

with open('integrations/llm.py', 'w', encoding='utf-8') as f:
    f.write(llm_code)

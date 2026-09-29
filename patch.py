import re

with open('pipeline.py', 'r', encoding='utf-8') as f:
    code = f.read()

imports = '''from agents.marketing_agent import MarketingAgent
from agents.copywriting_agent import CopywritingAgent
from agents.design_agent import DesignAgent
from agents.video_agent import VideoAgent
from agents.devops_agent import DevOpsAgent'''

# Remove dummy agents
code = re.sub(r'class BaseAgent:.*?class DevOpsAgent\(BaseAgent\): pass', imports, code, flags=re.DOTALL)

with open('pipeline.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('integrations/llm.py', 'r', encoding='utf-8') as f:
    llm_code = f.read()

llm_code = llm_code.replace('qwen/qwen-2.5-72b-instruct:free', 'meta-llama/llama-3.1-8b-instruct:free')

with open('integrations/llm.py', 'w', encoding='utf-8') as f:
    f.write(llm_code)

print('Patched successfully!')

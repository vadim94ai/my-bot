import asyncio
from agents.marketing_agent import MarketingAgent
async def main():
    agent = MarketingAgent()
    res = await agent.run()
    print('RESULT:', res)
asyncio.run(main())

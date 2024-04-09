import os

from langchain.agents import AgentType, initialize_agent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.tools import (
    ArxivQueryRun,
    DuckDuckGoSearchRun,
    Tool,
    WikipediaQueryRun,
)
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI

search = DuckDuckGoSearchRun()
arxiv = ArxivQueryRun()
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

llm = ChatOpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
prompt_template = "Write an essay for the topic provided by the user with the help of following content: {content}"
essay = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events.",
    ),
    Tool(
        name="Arxiv",
        func=arxiv.run,
        description="useful when you need an answer about encyclopedic general knowledge",
    ),
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="useful when you need an answer about encyclopedic general knowledge",
    ),
    Tool.from_function(
        func=essay.run,
        name="Essay",
        description="useful when you need to write an essay",
    ),
]
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

prompt = "Answer the user's question in helpful ways. Be helpful and honest. Question: {input}"
user_input = "When did World War II happen?"

answer = agent.invoke(prompt.format(input=user_input))
print(answer)

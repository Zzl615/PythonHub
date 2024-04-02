# import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.runnables import RunnablePassthrough, ConfigurableField

from langchain.globals import set_debug
set_debug(True)



# os.environ["LANGCHAIN_API_KEY"] = "..."
# os.environ["LANGCHAIN_TRACING_V2"] = "true"

prompt = ChatPromptTemplate.from_template(
    "请问'{topic}'是什么意思？"
)

wenxin_4_llm = QianfanChatEndpoint(
        model="ERNIE-Bot-4",
        temperature=0.1,
        max_tokens=512,
        model_kwargs={
            "top_p": 0.9,
            "top_k": 4,
            "repetition_penalty": 1.1,
            "presence_penalty": 0.2,
            "frequency_penalty": 0.2,
        },
        qianfan_ak="EKGrYLQJYjChZrbYsq0eoJd4",
        qianfan_sk="FGQ6VbZmWJ01uydwzionnhnobsdIqGBA"
)

zoegpt_model = ChatOpenAI(
    model="zoegpt_72b", 
    base_url="http://120.133.52.61:23008/v1",
    api_key="xxx",
    # request_timeout=1
)

model = (
    zoegpt_model
    .with_fallbacks([wenxin_4_llm])
    .configurable_alternatives(
        ConfigurableField(id="model"), 
        default_key="zoegpt_model", 
        wenxin_4_llm=wenxin_4_llm
    )
)

chain = (
    {"topic": RunnablePassthrough()} 
    |prompt 
    | model 
    | StrOutputParser()
)

output = chain.invoke(
    {"topic": "麻瓜"},
    config={"configurable": {"model": "wenxin_4_llm"}}
)

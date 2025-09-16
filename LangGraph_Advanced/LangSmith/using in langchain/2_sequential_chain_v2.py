from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os

os.environ['LANGCHAIN_PROJECT' ] = 'Sequential LLM App v2' # overwrite .env LANGCHAIN_PROJECT 

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
model2 = ChatOpenAI(model='gpt-4o', temperature=0.5)        # extra test using 2 model from v1 

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser



# custom run name ,tags,metadata 
# and can be others

config = {     
'run_name': 'sequential chain',
'tags': ['llm app', 'report generation', 'summarization'],
'metadata': {'model': 'gpt-4o-mini', 'model_temp':0.7, 'parser': 'stroutputparser'}
}



#passing config for customize output

result = chain. invoke({'topic': 'Unemployment in Nepal'}, config=config)    
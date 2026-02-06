from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# pip install langchain langchain-openai langchain-community sentence-transformers faiss-cpu

modelo = ChatOpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
    temperature=0.5,
    model="gpt-4o-mini"
)

#embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documento = TextLoader(
    "documentos/GTB_gold_Nov23.txt", 
    encoding="utf8"
).load()

pedacos = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100
).split_documents(documento)

dados_recuperados = FAISS.from_documents(
    pedacos, embeddings
).as_retriever(search_kwargs={"k":2})

prompt_consulta_seguro = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda apenas com base no contexto fornecido"),
        ("human", "{query}\n\nContexto: \n{context}\n\nResposta:"),
    ]
)

cadeia = prompt_consulta_seguro | modelo | StrOutputParser()

def responder(pergunta: str):
    trechos = dados_recuperados.invoke(pergunta)
    contexto = "\n\n".join([trecho.page_content for trecho in trechos])
    return cadeia.invoke({"query": pergunta, "context": contexto})

print(responder("Como devo proceder caso tenha um item roubado?"))
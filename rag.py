
#pip install -qU langchain-openai
#pip install langchain langchain_community langchain_chroma
#pip install bs4
#pip install rapidocr-onnxruntime
#pip install pymupdf


#from langchain import hub
#import getpass
#from langchain_core.output_parsers import StrOutputParser
#from langchain_core.runnables import RunnablePassthrough

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
import bs4
import os
from langchain_openai import ChatOpenAI
###########

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

###########

llm = ChatOpenAI(model="gpt-3.5-turbo")

''', extract_images=True'''

loader2 = PyPDFDirectoryLoader("test/")
docs2 = loader2.load()
#print(docs2[0])
'''
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader3 = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
    #https://ce.aut.ac.ir/persons.php?sid=1&slc_lang=fa
    #web_paths=("https://ce.aut.ac.ir/persons.php?sid=1&slc_lang=fa",),
)
docs3 = loader3.load()
print(docs3)

docs2.extend(docs3)
'''

######################################



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs2)#print(len(all_splits))
#print(type(all_splits))
#print(all_splits[1])

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
#test  retriever
#retrieved_docs = retriever.invoke("علت عدم مشاهده بعضی از دروس در لیست انتخاب واحد؟")

#print(len(retrieved_docs))
#print(retrieved_docs)

system_prompt = (
    "شما به‌عنوان یک دستیار برای پاسخ به پرسش‌ها فعالیت می‌کنید."
    "از بخش‌های زیر که از متن بازیابی شده‌اند برای پاسخ دادن به پرسش استفاده کنید."
    "اگر پاسخ را نمی‌دانید، بیان کنید که پاسخ را نمی‌دانید."
    "از حداکثر سه جمله استفاده کرده و پاسخ را مختصر ارائه دهید. "
    
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)


rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#response = rag_chain.invoke({"input": "شناسه موقت کاربری را چگونه میتوان دریافت کرد؟"})
#response = rag_chain.invoke({"input": "ثبت درخواست اصلاح کارنامه چگونه است؟"})

#print(response["answer"])


def query(text):
    
    response = rag_chain.invoke({"input": text})
    
    return response["answer"]

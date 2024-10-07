import os
from pathlib import Path
from typing import Union, Optional
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

load_dotenv()

FAISS_DB_DIR = os.getenv("FAISS_DB_DIR")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

faiss_db = FAISS.load_local(
    "vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True
)
llm_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000,
)


def get_retrieval_chain(faiss_db: FAISS, tag: Optional[str] = None) -> RetrievalQA:
    search_kwargs = {"k": 1}
    if tag:
        search_kwargs["filter"] = {"tag": tag}

    retrieval_chain = RetrievalQA.from_llm(
        llm=llm_model,
        retriever=faiss_db.as_retriever(
            search_type="similarity",
            search_kwargs=search_kwargs,
        ),
        return_source_documents=True,
    )
    return retrieval_chain


def rag_chatbot(
    input_text: str, tag: Optional[str] = None
) -> dict[str, Union[str, list[dict[str, any]]]]:
    retrieval_chain = get_retrieval_chain(faiss_db, tag)

    prompt = f"""
        You are an expert in urban planning. Provide a thorough explanation for the following question, using reliable sources if available:
        # input: {input_text}
        """
    response = retrieval_chain.invoke({"question": prompt, "query": input_text})
    source_details = []
    for document in response["source_documents"]:
        source_details.append(
            {
                "id": document.metadata["id"],
                #"source": document.metadata["source"],
                #"tag": document.metadata["tag"],
                "page_content": document.page_content,
            }
        )

    return {
        "result": response["result"],
        "source_details": source_details,
    }

if __name__ == "__main__":
    print(rag_chatbot(input_text="なんのドキュメントか教えてください"))
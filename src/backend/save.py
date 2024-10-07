import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.documents.base import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


load_dotenv()

FAISS_DB_DIR = "vectorstore"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# SOURCE_DICT = {
#     "1OPwETARiqhOveeod4fM5vjUlN8aZmBoW": "プロフィールスライド",
#     "1ZwhqVQI_jJ9MuTpkZk5g2NLj_coQiJP2": "AI活用領域スライド",
# }


def load_documents(data_dir: str) -> list[Document]:
    documents = []
    for path in Path(data_dir).glob("*.txt"):
        with open(path, "r") as f:
            text = f.read()
            document = Document(
                page_content=text,
                metadata={
                    "created_at": datetime.date.today(),
                    "id": Path(path).stem,
                    #"source": SOURCE_DICT[Path(path).stem],
                    #"tag": link_tag(text)["content"]["tag"],
                },
            )
            documents.append(document)
    return documents


def split_documents_to_chunk(documents: list[Document]) -> list[Document]:
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


def save_vector_store(chunked_documents: list[Document], save_dir: str) -> None:
    faiss_db = FAISS.from_documents(
        documents=chunked_documents,
        embedding=OpenAIEmbeddings(),
    )
    faiss_db.save_local(save_dir)
    print("Saving vector store completed.")


def save(data_dir: str) -> None:
    documents = load_documents(data_dir)
    chunked_documents = split_documents_to_chunk(documents)
    save_vector_store(chunked_documents, FAISS_DB_DIR)





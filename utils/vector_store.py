from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class VectorStore:
    def __init__(self):
        # Sentence-Transformers 임베딩 모델 (경량, 무료)
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.index = None

    def index_document(self, text):
        """
        문서를 청크 단위로 분리하고, 각 청크를 벡터화하여 FAISS DB에 저장
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = [Document(page_content=c) for c in splitter.split_text(text)]
        self.index = FAISS.from_documents(docs, self.embedding)

    def similarity_search(self, query, k=3):
        """
        질문 → 벡터화 → Top-K 유사 문서 검색
        """
        if self.index is None:
            return []
        return self.index.similarity_search(query, k=k)

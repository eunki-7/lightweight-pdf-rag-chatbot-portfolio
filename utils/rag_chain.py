from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

class RAGPipeline:
    def __init__(self, vector_store):
        self.vector_store = vector_store

        # 로컬 파이프라인 생성 (token 불필요)
        pipe = pipeline("text2text-generation", model="google/flan-t5-small")
        self.llm = HuggingFacePipeline(pipeline=pipe)

        self.qa_chain = None

    def _init_chain(self):
        if self.vector_store.index:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.vector_store.index.as_retriever(),
                return_source_documents=True
            )

    def query(self, question, threshold=0.6):
        if not self.vector_store.index:
            return self.llm(question), "No document indexed."

        if self.qa_chain is None:
            self._init_chain()

        result = self.qa_chain({"query": question})
        answer = result["result"]
        sources = result["source_documents"]

        if not sources:
            return self.llm(question), "No relevant context found."

        return answer, "\n\n".join([doc.page_content for doc in sources])

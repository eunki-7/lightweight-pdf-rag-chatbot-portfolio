import gradio as gr
from utils.pdf_loader import load_pdf
from utils.vector_store import VectorStore
from utils.rag_chain import RAGPipeline

# ---- VectorStore와 RAG 파이프라인 초기화 ----
vector_store = VectorStore()
rag_pipeline = RAGPipeline(vector_store)

def process_pdf(file):
    """
    PDF 파일을 읽어 텍스트 추출 → 벡터 DB 인덱싱
    """
    text = load_pdf(file.name)
    vector_store.index_document(text)
    return "PDF uploaded and indexed successfully."

def answer_question(query):
    """
    질문 처리 흐름:
    1) 벡터 검색
    2) threshold 이상 → 문서 기반 답변
    3) threshold 이하 → 모델 직접 추론 (Fallback)
    """
    answer, context = rag_pipeline.query(query)
    return answer, context

# ---- Gradio UI 구성 ----
with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("## DocuQuery AI – Lightweight PDF RAG Chatbot (with Fallback)")

    with gr.Row():
        with gr.Column():
            # 변경 (filepath 반환)
            pdf_file = gr.File(label="Upload PDF", type="filepath")
            upload_btn = gr.Button("Process PDF")
            output_upload = gr.Textbox(label="Upload Status")
        with gr.Column():
            question = gr.Textbox(label="Ask a question")
            answer_box = gr.Textbox(label="Answer")
            context_box = gr.Textbox(label="Top context chunks")
            submit_btn = gr.Button("Submit")

    upload_btn.click(process_pdf, inputs=[pdf_file], outputs=[output_upload])
    submit_btn.click(answer_question, inputs=[question], outputs=[answer_box, context_box])

if __name__ == "__main__":
    demo.launch()

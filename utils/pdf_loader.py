import fitz  # PyMuPDF

def load_pdf(file_path):
    """
    PDF 파일의 모든 페이지에서 텍스트 추출
    Args:
        file_path (str): PDF 파일 경로
    Returns:
        str: 전체 텍스트
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# Streamlit 앱 제목 설정
st.title("Gemini API를 이용한 PDF 분석")

# 사용자로부터 API 키 입력 받기
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

# PDF 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

# API 키가 입력되고 파일이 업로드되었을 때만 처리 진행
if api_key and uploaded_file:
    genai.configure(api_key=api_key)

    # PDF 파일 읽기
    def read_pdf(file):
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    pdf_text = read_pdf(uploaded_file)

    # Gemini 모델 설정
    model = genai.GenerativeModel('gemini-pro')

    # 사용자 입력 받기
    user_question = st.text_input("PDF에 대해 질문하세요:")

    if user_question:
        # Gemini API를 사용하여 답변 생성
        response = model.generate_content(f"다음 텍스트에 기반하여 질문에 답하세요: {pdf_text}\n\n질문: {user_question}")
        
        # 답변 출력
        st.write("답변:", response.text)
else:
    if not api_key:
        st.warning("API 키를 입력해주세요.")
    if not uploaded_file:
        st.warning("PDF 파일을 업로드해주세요.")

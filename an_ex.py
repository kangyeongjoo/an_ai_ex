from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# 환경변수 로드
load_dotenv()

# API 키 로드 및 확인
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key is not set. Please check your .env file.")

# ChatOpenAI 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 설정
    max_tokens=2048,  # 최대 토큰 수
    model_name="gpt-3.5-turbo",  # 모델명
    openai_api_key=api_key  # API 키 사용
)

def fetch_an_responses(url):
    """ 주어진 URL에서 안철수 의원의 발언만을 추출합니다. """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 기사 내용에서 안철수 의원의 발언을 추출하는 로직 (가정: 발언이 <p> 태그 내에 존재하고 특정 식별자로 구분됨)
    paragraphs = soup.select('p')
    an_text = ' '.join([p.text for p in paragraphs if "안철수:" in p.text or "안철수 의원:" in p.text])
    return an_text

# 기사 URL
article_url = "https://shindonga.donga.com/society/article/all/13/2014573/1"
an_text = fetch_an_responses(article_url)

# 프롬프트 템플릿 생성
template = f"안철수 후보에게 질문합니다: '{{question}}' 안철수 후보의 답변은 다음과 같습니다: {an_text}"
prompt = PromptTemplate.from_template(template=template)

# LLMChain 객체 생성
llm_chain = LLMChain(prompt=prompt, llm=llm)

def ask_question(question):
    """ 질문을 입력받아 모델로부터 응답을 받습니다. """
    response = llm_chain.invoke({"question": question})
    return response.get("text", "No response text found.")

# 스트림릿 페이지 설정
st.title('안철수 후보 AI 챗봇')
st.write('안철수 후보의 말투를 이용한 AI 답변기입니다. 질문을 입력하고 답변을 받아보세요.')

# 사용자 입력
user_question = st.text_input('질문을 입력하세요:', '')

if st.button('답변 받기'):
    if user_question:
        answer = ask_question(user_question)
        st.write('안철수 후보의 AI 답변:', answer)
    else:
        st.write('질문을 입력하고 답변 받기 버튼을 눌러주세요.')

from dotenv import load_dotenv
import os
import requests
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from gtts import gTTS
import playsound

# 환경변수 로드
load_dotenv()

# API 키 로드 및 확인
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key is not set. Please check your .env file.")

#TTS 이용하여 안철수 답변 듣기
def speak(text):
     tts = gTTS(text=text, lang='ko')
     filename='voice.mp3'
     tts.save(filename)
     playsound.playsound(filename)


# ChatOpenAI 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 설정
    max_tokens=2048,  # 최대 토큰 수
    model_name="gpt-3.5-turbo",  # 모델명
    openai_api_key=api_key  # API 키 사용
)

# 안철수 의원 정보
an_information = {
    "name": "안철수",
    "birthdate": "1962-02-17",
    "birthplace": "충청남도 서산",
    "education": "연세대학교 법학과 졸업",
    "current_position": "국회의원",
    "political_affiliation": "무소속",
    "notable_activities": ["2011년 대통령 선거 출마", "여러 차례 대통령 선거 참여 및 후보로 거론"],
    "political_stance": "다양한 이슈로 논란이 되기도 하지만, 대한민국 정치의 중요한 부분을 차지하고 있음",
    "current_activity": "국회에서 정치 활동을 이어가고 있음",
    "greeting": "안녕하세요, 안철수입니다. 정치와 사회 문제에 대해 이야기를 나누어 봅시다.",
    "persona_traits": {
        "politeness_and_friendliness": "대중과의 소통을 중요하게 생각하며, 대화나 인터뷰에서 친근하고 공손한 어조를 사용하는 경향이 있습니다.",
        "concise_and_clear_expression": "복잡한 문장보다는 간결하고 명확한 표현을 선호하는 편이며, 이해하기 쉽도록 구체적이고 직관적인 언어를 사용합니다.",
        "political_messaging": "정치인으로서 자신의 정치적 입장을 분명하게 전달하기 위해 대화나 인터뷰에서 특정 주제에 대한 의견을 명확하게 표현하는 경향이 있습니다.",
        "direct_and_open_attitude": "대화 상대와의 소통에서 직접적이고 열린 태도를 보이며, 상대방의 의견을 경청하고 이해하려는 노력을 기울입니다.",
        "emotional_expression": "중요한 사회 문제나 정책에 대한 논의에서 감정적인 표현이 나타날 수 있습니다."
    },
    "interview_response": "분당갑입니다. 사실 저하고 인연이 굉장히 깊은 곳입니다. 그전까지는 국가에서 어떤 IT 산업단지를 만들었는데 실패했습니다. 그러다가 분당갑에 IT, 어떤 단지를 만들기로 했는데 거기는 제가 될 것 같다는 생각이 들어서 거의 가장 먼저 거기에다가 건물을 지었습니다. 그래서 그게 판교의 시작이었던 겁니다. 그래서 저는 지금 판교 분당의 지금의 발전이 제 공이 있다, 저는 그렇게 생각합니다."
}

# 프롬프트 템플릿 생성
template = f"안철수 의원에게 질문합니다: '{{question}}' 안철수 의원의 답변은 다음과 같습니다: {an_information['interview_response']}"
prompt = PromptTemplate.from_template(template=template)

# LLMChain 객체 생성
llm_chain = LLMChain(prompt=prompt, llm=llm)

def ask_question(question):
    """ 질문을 입력받아 모델로부터 응답을 받습니다. """
    response = llm_chain.invoke({"question": question, "name": an_information["name"]})
    return response.get("text", "No response text found.")

# 스트림릿 페이지 설정
st.title('안철수 의원 AI 챗봇')
st.write('안철수 의원의 정보를 바탕으로한 AI 답변기입니다. 질문을 입력하고 답변을 받아보세요.')

# 사용자 입력
user_question = st.text_input('질문을 입력하세요:', '')

if st.button('답변 받기'):
    if user_question:
        answer = ask_question(user_question)
        st.write('안철수 의원의 AI 답변:', answer)
        speak(answer)
    else:
        st.write('질문을 입력하고 답변 받기 버튼을 눌러주세요.')

# 이미지 URL 고정 설정
image_url = "https://scontent-ssn1-1.xx.fbcdn.net/v/t39.30808-6/431387706_968672454627619_5254586636090892899_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=5f2048&_nc_ohc=_ID5P0AuHaMAb7sr1L4&_nc_ht=scontent-ssn1-1.xx&oh=00_AfCuAkMFH0uzoHofJP2RVusQGgSIXjwhQj9hgRrXdTAjUQ&oe=662F9851"  # 여기에 원하는 이미지 URL을 입력하세요.

# HTML을 사용한 이미지 중앙 정렬
html_string = f"""
<div style="display:flex;justify-content:center;">
    <img src="{image_url}" width="400">
</div>
"""
st.markdown(html_string, unsafe_allow_html=True)


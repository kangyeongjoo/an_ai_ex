# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

import os

print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}")

import openai

openai.__version__

from langchain_openai import ChatOpenAI

# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    max_tokens=2048,  # 최대 토큰수
    model_name="gpt-3.5-turbo",  # 모델명
)

# 질의내용
question = "대한민국의 수도는 어디인가요?"

# 질의
print(f"[답변]: {llm.invoke(question)}")

# 질의내용
question = "대한민국의 대통령은 누구인가요?"

# 질의
print(f"[답변]: {llm.invoke(question)}")

# 질의내용
question = "안철수가 가장 현재 관심가질만한 뉴스거리에 대해서 안철수 말투로 얘기해줘?"

# 질의
print(f"[답변]: {llm.invoke(question)}")

print(f"\n")
print(f"프롬프트 템플릿의 활용================")
#====================프롬프트 템플릿의 활용()
from langchain.prompts import PromptTemplate

# 질문 템플릿 형식 정의
template = "{country}의 수도는 뭐야?"

# 템플릿 완성
prompt = PromptTemplate.from_template(template=template)
prompt

#====================LLMChain 객체
from langchain.chains import LLMChain

# 연결된 체인(Chain)객체 생성
llm_chain = LLMChain(prompt=prompt, llm=llm)
llm_chain.invoke({"country": "대한민국"})
llm_chain.invoke({"country": "캐나다"})

#====================apply()
input_list = [{"country": "호주"}, {"country": "중국"}, {"country": "네덜란드"}]

response = llm_chain.apply(input_list)
response[0]["text"]

# input_list 에 대한 결과 반환
result = llm_chain.apply(input_list)

# 반복문으로 결과 출력
for res in result:
    print(res["text"].strip())






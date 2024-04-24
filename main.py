import pandas as pd 
import streamlit as st

#DB 연동 import
from database import SessionLocal, engine
from models import Todo

# DB 세션 초기화
def get_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# 데이터베이스에서 데이터 가져오기
def get_todos():
    db = next(get_db_session())
    todos = db.query(Todo).all()
    return todos

# 데이터를 DataFrame으로 변환
def todos_to_dataframe(todos):
    return pd.DataFrame([{'Task': todo.task, 'Completed': todo.completed} for todo in todos])

# 메인 함수
def main():
    todos = get_todos()
    df_todos = todos_to_dataframe(todos)

    st.subheader('Todo List from MySQL Database')
    st.table(df_todos)

if __name__ == "__main__":
    main()


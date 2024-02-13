from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time

load_dotenv()

# API_KEY=os.environ['OPENAI_API_KEY']
# client = OpenAI(api_key=API_KEY)

API_KEY=os.environ['OPENAI_API_KEY']
openai_key=API_KEY

# assistant_id 생성코드
# assistant = client.beta.assistants.create(
#     name="내부 직원 프롬프트 테스트",
#     instructions="너는 기업에서 일하는 직원이야. 너의 역할은 재무부정을 방지하기 위해 내부통제 위험요소를 파악하고 전표의 데이터에 오류나 누락이 없는지 확인하는 거야. 재무 관련 데이터와 오류 여부를 확인할 수 있는 기준을 첨부파일로 같이 줄거야. 그 파일 내에서 정확하게 일치하는 부분을 찾아서 답변해줘.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4-turbo-preview",
#     file_ids=["file-UBE2kh3ae95at1sokPJAdr2V"]
# )    
# print(assistant)

# thread_id, assistant_id 설정
thread_id = "thread_5OwySoM21wXjTNrAU1NaXCcZ"
assistant_id = "asst_x3aeIz36Q5NptIOIb5NhIwxK" #개인 계정에 생성된 어시스턴스

prompt = st.chat_input("내용을 입력하세요.")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    #입력한 메세지 UI에 표시
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    # run 실행
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="너는 조만간 외부감사인에게 감사를 받게 될거야. 내가 업로드한 파일에서만 찾은 답변을 해줘. 만약, 업로드한 파일내에서 정보를 찾을 수 없으면 거기에서 답변 생성을 멈춰도되. 목록이 5줄 이상이 되면 목록 제목이 가로로 된 표로 정리해줘."
    )

    with st.spinner("응답을 기다리고 있습니다."):
        # run 상태 체크
        while run.status != "completed":
            print("확인 중 :",run.status)
            time.sleep(0.2)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    #whlie 에서 빠져와 msg 불러오기
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # 마지막 메세지에 UI 추가하기
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
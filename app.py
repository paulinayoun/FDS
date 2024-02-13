#################################################################################
# FDS
# Original Service https://chat2vis.streamlit.app/
# Original work by @frog-land. Modified by @paulinayoun.
#################################################################################
from dotenv import load_dotenv
import os
import pandas as pd
import openai
from openai import OpenAI
import streamlit as st
#import streamlit_nested_layout
from classes import get_primer,format_question,run_request
import warnings
import time
load_dotenv()

API_KEY=os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="💰",layout="wide",page_title="FDS 테스트 페이지")

st.markdown("<h4 style='text-align: center;padding-top: 0rem;'>테스트</h4>", unsafe_allow_html=True)

available_models = {"ChatGPT-3.5": "gpt-3.5-turbo"}

# available_models = {"ChatGPT-3.5": "gpt-3.5-turbo", "GPT-3.5 Instruct": "gpt-3.5-turbo-instruct"}

# List to hold datasets
if "datasets" not in st.session_state:
    datasets = {}
    # Preload datasets
    datasets["총계정원장"] =pd.read_csv("files\glsample.csv")
    st.session_state["datasets"] = datasets
else:
    # use the list already loaded
    datasets = st.session_state["datasets"]


with st.sidebar:
    # First we want to choose the dataset, but we will fill it with choices once we've loaded one
    dataset_container = st.empty()

    # Add facility to upload a dataset
    try:
        uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")
        index_no=0
        if uploaded_file:
            # Read in the data, add it to the list of available datasets. Give it a nice name.
            file_name = uploaded_file.name[:-4].capitalize()
            datasets[file_name] = pd.read_csv(uploaded_file)
            # We want to default the radio button to the newly added dataset
            index_no = len(datasets)-1
    except Exception as e:
        st.error("File failed to load. Please select a valid CSV file.")
        print("File failed to load.\n" + str(e))
    # Radio buttons for dataset choice
    chosen_dataset = dataset_container.radio(":bar_chart: 데이터를 선택하세요:",datasets.keys(),index=index_no)#,horizontal=True,)

    # Check boxes for model choice
    st.write(":brain: 현재는 GPT-3.5만 지원합니다.:")
    # Keep a dictionary of whether models are selected or not
    use_model = {}
    for model_desc,model_name in available_models.items():
        label = f"{model_desc} ({model_name})"
        key = f"key_{model_desc}"
        use_model[model_desc] = st.checkbox(label,value=True,key=key)
 
# Text area for query
question = st.text_area(":eyes: 무얼 도와드릴까요?",height=10)
go_btn = st.button("생성")

# Make a list of the models which have been selected
selected_models = [model_name for model_name, choose_model in use_model.items() if choose_model]
model_count = len(selected_models)

thread_id = "thread_5OwySoM21wXjTNrAU1NaXCcZ"
assistant_id = "asst_x3aeIz36Q5NptIOIb5NhIwxK" #개인 계정에 생성된 어시스턴스






# Execute chatbot query
if go_btn and model_count > 0:
    api_keys_entered = True
    # Check API keys are entered.
    if api_keys_entered:
    # Place for plots depending on how many models
        plots = st.columns(model_count)
        # Get the primer for this dataset
        primer1,primer2 = get_primer(datasets[chosen_dataset],'datasets["'+ chosen_dataset + '"]') 
        # Create model, run the request and print the results
        for plot_num, model_type in enumerate(selected_models):
            with plots[plot_num]:
                st.subheader(model_type)
                try:
                    # Format the question
                    question_to_ask = format_question(primer1, primer2, question, model_type)
                    # Run the question
                    answer=""
                    answer = run_request(question_to_ask, available_models[model_type], key=client)
                    # the answer is the completed Python script so add to the beginning of the script to it.
                    answer = primer2 + answer
                    print("Model: " + model_type)
                    print(answer)
                    plot_area = st.empty()
                    plot_area.pyplot(exec(answer))           
                except Exception as e:
                    if type(e) == openai.APIError:
                        st.error("OpenAI API Error. Please try again a short time later. (" + str(e) + ")")
                    elif type(e) == openai.Timeout:
                        st.error("OpenAI API Error. Your request timed out. Please try again a short time later. (" + str(e) + ")")
                    elif type(e) == openai.RateLimitError:
                        st.error("OpenAI API Error. You have exceeded your assigned rate limit. (" + str(e) + ")")
                    elif type(e) == openai.APIConnectionError:
                        st.error("OpenAI API Error. Error connecting to services. Please check your network/proxy/firewall settings. (" + str(e) + ")")
                    elif type(e) == openai.APIResponseValidationError:
                        st.error("OpenAI API Error. Your request was malformed or missing required parameters. (" + str(e) + ")")
                    elif type(e) == openai.AuthenticationError:
                        st.error("Please enter a valid OpenAI API Key. (" + str(e) + ")")
                    elif type(e) == openai.OpenAIError:
                        st.error("OpenAI Service is currently unavailable. Please try again a short time later. (" + str(e) + ")")               
                    else:
                        st.error("Unfortunately the code generated from the model contained errors and was unable to execute.")

# Display the datasets in a list of tabs
# Create the tabs
tab_list = st.tabs(datasets.keys())

# Load up each tab with a dataset
for dataset_num, tab in enumerate(tab_list):
    with tab:
        # Can't get the name of the tab! Can't index key list. So convert to list and index
        dataset_name = list(datasets.keys())[dataset_num]
        st.subheader(dataset_name)
        st.dataframe(datasets[dataset_name],hide_index=True)

# Insert footer to reference dataset origin  
footer="""<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;text-align: center;}</style><div class="footer">
<p> <a style='display: block; text-align: center;'> Original work by @frog-land. Modified by @paulinayoun. </a></p></div>"""
st.caption("Original work by @frog-land. Modified by @paulinayoun.")

# Hide menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# Text area for query
# question = st.text_area(":eyes: 무얼 도와드릴까요?",height=10)
# go_btn = st.button("생성")

prompt = st.chat_input("내용을 입력하세요.")
if prompt and model_count > 0:
    api_keys_entered = True
    # Check API keys are entered.
    if api_keys_entered:
    # Place for plots depending on how many models
        plots = st.columns(model_count)
        # Get the primer for this dataset
        primer1,primer2 = get_primer(datasets[chosen_dataset],'datasets["'+ chosen_dataset + '"]') 
        # Create model, run the request and print the results
        for plot_num, model_type in enumerate(selected_models):
            with plots[plot_num]:
                st.subheader(model_type)
                try:
                    # Format the question
                    question_to_ask = format_question(primer1, primer2, question, model_type)
                    # Run the question
                    answer=""
                    answer = run_request(question_to_ask, available_models[model_type], key=client)
                    # the answer is the completed Python script so add to the beginning of the script to it.
                    answer = primer2 + answer
                    print("Model: " + model_type)
                    print(answer)
                    plot_area = st.empty()
                    plot_area.pyplot(exec(answer))           
                except Exception as e:
                    if type(e) == openai.APIError:
                        st.error("OpenAI API Error. Please try again a short time later. (" + str(e) + ")")
                    elif type(e) == openai.Timeout:
                        st.error("OpenAI API Error. Your request timed out. Please try again a short time later. (" + str(e) + ")")
                    elif type(e) == openai.RateLimitError:
                        st.error("OpenAI API Error. You have exceeded your assigned rate limit. (" + str(e) + ")")
                    elif type(e) == openai.APIConnectionError:
                        st.error("OpenAI API Error. Error connecting to services. Please check your network/proxy/firewall settings. (" + str(e) + ")")
                    elif type(e) == openai.APIResponseValidationError:
                        st.error("OpenAI API Error. Your request was malformed or missing required parameters. (" + str(e) + ")")
                    elif type(e) == openai.AuthenticationError:
                        st.error("Please enter a valid OpenAI API Key. (" + str(e) + ")")
                    elif type(e) == openai.OpenAIError:
                        st.error("OpenAI Service is currently unavailable. Please try again a short time later. (" + str(e) + ")")               
                    else:
                        st.error("Unfortunately the code generated from the model contained errors and was unable to execute.")
    print(prompt)
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
#         st.image(image_path, caption="Image Caption")

# file_id = file_id
# image_path = download_image(file_id)

# def download_image(file_id)
# # MessageContentImageFile(image_file=ImageFile(file_id='file-9Blij8vAGdLXr3IkTH3yKoTR'), type='image_file')
        
# # 이미지 파일 ID를 사용하여 이미지 파일을 다운로드하는 코드 추가 (예시 코드, 실제 구현은 API에 따라 다를 수 있음)
# # file_id = 'file-9Blij8vAGdLXr3IkTH3yKoTR'
# # image_path = download_image(file_id) # download_image는 이미지를 다운로드하는 함수, 실제 구현 필요

# # 이미지 파일을 UI에 표시
# # with st.chat_message(role):
# #     st.image(image_path, caption="Image Caption") # 이미지 경로와 캡션 설정
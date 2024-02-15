#################################################################################
# FDSsupporting functions
# Original Service https://chat2vis.streamlit.app/
# Original work by @frog-land. Modified by @paulinayoun.
#################################################################################
from dotenv import load_dotenv
import os
import pandas as pd
import openai
from openai import OpenAI
from langchain import HuggingFaceHub, LLMChain,PromptTemplate
load_dotenv()

API_KEY=os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

def run_request(question_to_ask, model_type, key):

    if model_type == "gpt-4" or model_type == "gpt-3.5-turbo" :
        # Run OpenAI ChatCompletion API
        task = "Generate Python Code Script."
        task = task + "당신은 재무 기록에서 이상 징후를 감지하는 데 훈련된 AI입니다. 당신의 역할은 재무부정을 방지하기 위해 내부통제 위험요소를 파악하고 전표의 데이터에 오류나 누락이 없는지 확인하는 것입니다. 출납 내역이 기록된 총계정원장 파일을 첨부파일로 같이 줄 것입니다. 그 파일 내에서 정확하게 일치하는 부분을 찾아서 답변하십시오. "
        openai.api_key = key
        response = client.chat.completions.create(
            model=model_type,
            messages=[
                {
                    "role":"system","content":task
                },
                {
                    "role":"user","content":question_to_ask
                }
            ],
            temperature=0.1,
        )
        llm_response = response.choices[0].message.content
        print(llm_response)
    # rejig the response
    llm_response = format_response(llm_response)
    return llm_response

def format_response( res):
    # Remove the load_csv from the answer if it exists
    csv_line = res.find("read_csv")
    if csv_line > 0:
        return_before_csv_line = res[0:csv_line].rfind("\n")
        if return_before_csv_line == -1:
            # The read_csv line is the first line so there is nothing to need before it
            res_before = ""
        else:
            res_before = res[0:return_before_csv_line]
        res_after = res[csv_line:]
        return_after_csv_line = res_after.find("\n")
        if return_after_csv_line == -1:
            # The read_csv is the last line
            res_after = ""
        else:
            res_after = res_after[return_after_csv_line:]
        res = res_before + res_after
    return res

def format_question(primer_desc,primer_code , prompt, model_type):
    # Fill in the model_specific_instructions variable
    instructions = ""
    if model_type == "Code Llama":
        # Code llama tends to misuse the "c" argument when creating scatter plots
        instructions = "\nDo not use the 'c' argument in the plot function, use 'color' instead and only pass color names like 'green', 'red', 'blue'."
    primer_desc = primer_desc.format(instructions)  
    # Put the question at the end of the description primer within quotes, then add on the code primer.
    return  '"""\n' + primer_desc + prompt + '\n"""\n' + primer_code

def get_primer(df_dataset,df_name):
    # Primer function to take a dataframe and its name
    # and the name of the columns
    # and any columns with less than 20 unique values it adds the values to the primer
    # and horizontal grid lines and labeling
    primer_desc = "Use a dataframe called df from data_file.csv with columns '" \
        + "','".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i]=="O":
            primer_desc = primer_desc + "\nThe column '" + i + "' has categorical values '" + \
                "','".join(str(x) for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i]=="int64" or df_dataset.dtypes[i]=="float64":
            primer_desc = primer_desc + "\nThe column '" + i + "' is type " + str(df_dataset.dtypes[i]) + " and contains numeric values. "   
    primer_desc = primer_desc + "\nLabel the x and y axes appropriately."
    primer_desc = primer_desc + "\nAdd a title. Set the fig suptitle as empty."
    primer_desc = primer_desc + "{}" # Space for additional instructions if needed
    primer_desc = primer_desc + "\nUsing Python version 3.9.12, create a script using the dataframe df to graph the following: "
    pimer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    pimer_code = pimer_code + "fig,ax = plt.subplots(1,1,figsize=(12,5))\n"
    pimer_code = pimer_code + "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False) \n"
    pimer_code = pimer_code + "df=" + df_name + ".copy()\n"
    return primer_desc,pimer_code
import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
                                                  ConversationSummaryMemory,
                                                  ConversationBufferWindowMemory
                                                  )

if 'conversation' not in st.session_state:
    st.session_state['conversation']=None 

if ['messages'] not in st.session_state:
    st.session_state['messages']= []
     
if ['API_Key'] not in st.session_state:
    st.session_state['API_Key']= ''

st.set_page_config(page_title="CHATGPT 3.5-Turbo", page_icon="😊")
st.markdown("<h1 style='text-align: center;'>😊GPT 3.5 Turbo</h1>", unsafe_allow_html=True)

st.sidebar.title("First paste here your Api Key")
st.session_state['API_Key']= st.sidebar.text_input("What's your API KEY?", type= "password")
summerize_button = st.sidebar.button("Summerize the conversation", key="summerize")
if summerize_button:
    summerize_placeholder = st.sidebar.write("Nice chatting with you my friend 🖤:\n\n"+"Hello Friend")
      
def getresponse(userInput, api_key):

    if st.session_state['conversation'] is None:

        llm = OpenAI( 
            temperature=0,
            openai_api_key= api_key,
            model_name= "text-davinci-003"
            )

        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response = st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)

    return response


response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        prompt = st.text_input("Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label='send')
        if submit_button:
            st.session_state['messages'].append(prompt)
            model_response = getresponse(prompt, st.session_state['API_Key'])
            st.session_state['messages'].append(model_response)
            

            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')


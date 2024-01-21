
import os

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from st_multimodal_chatinput import multimodal_chatinput
import streamlit as st


st.title("Multimodal Chat w/ Gemini")
st.image("gemini.jpeg")


# Set Google API key
GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)


# make model
model = genai.GenerativeModel('gemini-pro')
vision_model = ChatGoogleGenerativeAI(model="gemini-pro-vision")


# having trouble with chat input box, always in the middle of chat https://github.com/het-25/st-multimodal-chatinput
def reconfig_chatinput():
  st.markdown(
      """
  <style>
  {
          width: 100%; /* Span the full width of the viewport */;
          background-color: #FFC0CB;
          }
  </style>
  """,
      unsafe_allow_html=True,
  )
  return

reconfig_chatinput()

# seed msg, init chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask Gemini anything || send pic w/ a prompt!"
        }
    ]

# display chat msgs from history upon rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# process, store query + resp
def call_llm_just_text(q):
  response = model.generate_content(q)

  # display assistant msg
  with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGVfLdUg7kVxuSqqBGgAL3UJeQgRCLPhxIZlXbVxmUAdYaJm-fcUal7x-FHhwxzpeg6_M&usqp=CAU"):
    st.markdown(response.text)

  # store user msg
  st.session_state.messages.append(
    {
      "role":"user",
      "content": q
    }
  )

  # store assistant msg
  st.session_state.messages.append(
    {
      "role":"assistant",
        "content": response.text
    }
  )

# process, store query + resp
def call_llm_with_img(q):
  with st.spinner('Processing📈...'):
    uploaded_images = q["images"] # list of base64 encodings of uploaded imgs
    txt_inp = q["text"] # submitted text
    msg = HumanMessage(
      content=[
        {
          "type": "text",
          "text": txt_inp,
        },
        {
          "type": "image_url",
          "image_url": uploaded_images[0]
        },
      ]
    )
    resp = vision_model.invoke([msg])

  # display assistant msg
  with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGVfLdUg7kVxuSqqBGgAL3UJeQgRCLPhxIZlXbVxmUAdYaJm-fcUal7x-FHhwxzpeg6_M&usqp=CAU"):
    st.markdown(resp.content)

  # store user msg
  st.session_state.messages.append(
    {
      "role":"user",
      "content": txt_inp
    }
  )

  # store assistant msg
  st.session_state.messages.append(
    {
      "role":"assistant",
        "content": resp.content
    }
  )

user_inp = multimodal_chatinput() # multimodal streamlit chat input

# call llm funcs when input is given
if user_inp:
    # display user msg
    with st.chat_message("user", avatar="https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/000/517/300/datas/profile.png"):
        st.markdown(user_inp["text"])

    # check if just text
    if len(user_inp["images"]) == 0:
      call_llm_just_text(user_inp["text"])

    # user_inp includes image
    else: 
      call_llm_with_img(user_inp)

st.markdown(
    """
    <div>
    <p style="text-align: center;font-family:Arial; color:Pink; font-size: 12px;display: table-cell; vertical-align: bottom">Made with ❤️ in SF. ✅ out <a href="https://replit.com/@LizzieSiegle/gemini-multimodal-chat">the repl!</a></p>
    </div>
    """,
    unsafe_allow_html=True, # HTML tags found in body escaped -> treated as pure text
)
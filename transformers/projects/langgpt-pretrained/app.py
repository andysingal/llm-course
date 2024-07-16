import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="LangGPT",
)

from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

repo_name = "shinigami-srikar/langgpt-pretrained"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(repo_name)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(repo_name)
    return tokenizer, model

tokenizer, model = load_model()

def translate_text(text):
    input_ids = tokenizer(text, return_tensors="tf", padding=True ,max_length=128, truncation=True).input_ids
    outputs = model.generate(input_ids)
    translations = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translations[0]

st.title("LangGPT")

st.write("This app translates English text to Hindi using a custom transformer model hosted on Hugging Face and trained on the OPUS dataset.")

text = st.text_area("Enter some English text")

if 'translate_clicked' not in st.session_state:
    st.session_state['translate_clicked'] = False

if st.button("Translate"):
    st.session_state['translate_clicked'] = True

if st.session_state['translate_clicked']:
    if text:
        # if len(text) > 
        with st.spinner("Translating..."):
            translation = translate_text(text)
        st.text_area("Hindi Translation:", translation)
    else:
        st.write("Please enter some text to translate.")


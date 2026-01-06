import validators
import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from langchain_classic.prompts import PromptTemplate
## streamli app setup
st.set_page_config(page_title="Langchain : Summarize text from youtube or Website",page_icon="🦜")
st.title("🦜Langcahin : Summarize text from youtube or website")
st.subheader('Summarize URL')

with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",value="",type="password")

generice_url = st.text_input("URL",label_visibility="collapsed")

if groq_api_key:
    llm = ChatGroq(groq_api_key=groq_api_key,model="llama-3.1-8b-instant")
##llm model


prompt_template="""
Provide a summary of the following content in 300 words:
Context:{text} 
"""

prompt=PromptTemplate(template=prompt_template,input_variables=['text'])

if st.button("Summarize the content from YT or Website"):
    if not groq_api_key.strip() or not generice_url.strip():
        st.error("Please provide the information to get started")

    elif not validators.url(generice_url):
        st.error("Please enter  a valid url. It can may be a youtube video url or website url")   

    else:
        try:
            with st.spinner("Waiting......."):
                if "youtube.com" in generice_url:
                    loader=YoutubeLoader.from_youtube_url(generice_url,add_video_info=False)   
                else:
                    loader=UnstructuredURLLoader(urls=[generice_url],ssl_verify=False,
                                                headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
                    )   
                docs=loader.load()

                chain = load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)      
                st.success(output_summary)
        except Exception as e:
            st.exception(e)          
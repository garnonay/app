import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile
import pytube
import re
# from transformers import pipeline


col,col1 = st.columns([1,8])
with col1:
    st.title("Instant Audio Transcription")
    st.markdown(
    """
    by Javier Garcia Nonay
    <a href="https://www.linkedin.com/in/javier-garcia-nonay/" rel="nofollow noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 35 35" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
            <path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"></path>
        </svg>
    </a>
    """,
    unsafe_allow_html=True
    )

@st.cache(show_spinner=False)
def load_whisper_model():
    model = whisper.load_model('base')
    return model

def valid_url(url):
 return re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url)

# @st.cache(show_spinner=False)
# def summarymodel():
#     summarizer = pipeline("summarization", model="t5-base")
#     return summarizer

# def summarize(text):
#   b = summarizer(text)
#   b = b[0]['summary_text']
#   return b

option = st.sidebar.selectbox('Options', ['Please choose one', 'Microphone', 'Audio file', 'Youtube Video'])
if option == 'Microphone':
    st.write('')
    st.write('')
    recording = audio_recorder()
    if recording:
        st.markdown("## 🔊 Audio")
        st.audio(recording, format="audio/wav")
        temp_file = NamedTemporaryFile().name
        with open(temp_file, mode='wb') as f:
            f.write(recording)
        st.markdown("## 📄 Transcription")
        #result = model.transcribe("myfile.wav", task='translate')
        with st.spinner("Transcribing audio..."):
            result = None
            try:
                model = load_whisper_model()
                result = model.transcribe(temp_file, fp16=False)
                st.write(result['text'])
            except RuntimeError:
                result = None
                st.warning(
                    """
                    Oops! Something went wrong. Please try again in a few seconds.
                    """
                )
elif option == 'Audio file':
    st.write('')
    st.write('')
    audio_file = st.file_uploader('Upload the file',type=['mp3', 'wav', 'aac', 'flac', 'm4a'])
    if audio_file:
        if audio_file is not None:
            st.markdown("## 🔊 Audio")
            recording = audio_file.read()
            st.audio(recording, format="audio/wav")
            temp_file1 = NamedTemporaryFile().name
            with open(temp_file1, mode='wb') as f:
                f.write(recording)
            st.markdown("## 📄 Transcription")
            #result = model.transcribe("myfile.wav", task='translate')
            with st.spinner("Transcribing audio..."):
                result = None
                try:
                    model = load_whisper_model()
                    result = model.transcribe(temp_file1, fp16=False)
                    st.write(result['text'])
                except RuntimeError:
                    result = None
                    st.warning(
                        """
                        Oops! Something went wrong. Please try again in a few seconds.
                        """
                    )
elif option == 'Youtube Video':
    st.write('')
    st.write('')
    url = st.text_input('Video URL')
    if url:
        right_url = valid_url(url)
        if right_url:
            st.markdown("## 🔊 Audio")
            data = pytube.YouTube(url)
            temp_file2 = NamedTemporaryFile().name
            audio_stream = data.streams.filter(only_audio=True).first()
            ytrecording = audio_stream.download(filename=temp_file2)
            st.audio(ytrecording, format="audio/wav")
            st.markdown("## 📄 Transcription")
            with st.spinner("Transcribing audio..."):
                result = None
                try:
                    model = load_whisper_model()
                    result = model.transcribe(ytrecording, fp16=False)
                    st.write(result['text'])
                except RuntimeError:
                    result = None
                    st.warning(
                        """
                        Oops! Something went wrong. Please try again in a few seconds.
                        """
                    )
            # if st.button('Summarize it please!'):
            #     model = summarymodel()
            #     summary = summarize(result['text'])
            #     st.write('Summary: ' + summary)
        else:
            st.warning("Invalid YouTube URL")

else:
    st.write('')
    st.write('')
    st.markdown(
        """
        This Streamlit app lets you transcribe YouTube videos using 
        [Whisper](https://github.com/openai/whisper), 
        a general-purpose speech recognition model developed by 
        [OpenAI](https://openai.com/).
        """
    )

import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile


col,col1 = st.columns([3,8])
with col1:
    st.title("Chat inteligente")
st.write('¿Cómo quieres interactuar con la IA?')

with st.expander("Con tu voz"):
    recording = audio_recorder()
    if recording:
        st.audio(recording, format="audio/wav")
        temp_file = NamedTemporaryFile().name
        with open(temp_file, mode='bw') as f:
            f.write(recording)
        model = whisper.load_model("base")
        #result = model.transcribe("myfile.wav", task='translate')
        result = model.transcribe(temp_file, language='es')
        st.write('Has dicho: ' + result['text'])

with st.expander("Subiendo un fichero"):
    audio_file = st.file_uploader('Sube el fichero de audio')
    if audio_file:
        if audio_file is not None:
            recording = audio_file.read()
        st.audio(recording, format="audio/wav")
        temp_file1 = NamedTemporaryFile().name
        with open(temp_file1, mode='bw') as f:
            f.write(recording)
        model = whisper.load_model("base")
        #result = model.transcribe("myfile.wav", task='translate')
        result = model.transcribe(temp_file1)
        st.write('El audio dice: ' + result['text'])
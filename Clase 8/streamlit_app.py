""" MI MODELO CHATGPT """ 

"Mi CHATGPT"
import streamlit as st
from groq import Groq 



modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
modelo_elegido = st.sidebar.selectbox("selecciona un modelo", modelos)


def crear_usuario_groq(): 
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)



def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []



def actualizar_historial(rol, contenido, avatar):
        st.session_state.mensajes.append(
            {"role": rol, "content": contenido, "avatar": avatar})
    

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]): st.markdown(mensaje["content"])
 
def area_chat():
    contenedorChat = st.container()  
    with contenedorChat: mostrar_historial()    
        




def main():
    clienteUsario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("¡Escribí tu mensaje!")   
    if mensaje:
        actualizar_historial("user", mensaje, "🧓🏻")       
        with st.chat_message("assistant", avatar = "🤖"):
            mensaje_respuesta = st.empty
            respuesta_completa = "" 
         #              
            respuesta_stream = clienteUsario.chat.completions.create(
                model = modelo_elegido,
                messages = [{"role": "user", "content": mensaje}],
                stream = True
            )
        
            for frase in respuesta_stream:
                if frase.choices[0].delta.content:
                    respuesta_completa += frase.choices[0].delta.content
            st.markdown(respuesta_completa)
        
            actualizar_historial("assistant", respuesta_completa, "🤖")
            st.rerun()

main()


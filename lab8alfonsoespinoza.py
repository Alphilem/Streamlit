import streamlit as st
from openai import OpenAI
import pandas as pd

# ✅ Obtener API key desde los secretos de Streamlit
api_key = st.secrets["OPENAI_API_KEY"]

# Inicializar cliente OpenAI
client = OpenAI(api_key=api_key)

# Importar dataset
df = pd.read_csv('anime.csv')

# Usar solo las primeras 150 filas
df_subset = df.head(150)

# Convertir a texto
df_string = df_subset.to_string()

# Título
st.title("Recomendador de Anime⛩️")

# Campo de texto para la pregunta
user_input = st.text_input("Escribe tu pregunta sobre anime:")

# Cuando el usuario escribe una pregunta
if user_input:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en anime y recomendaciones de anime. "
                    "Usa ÚNICAMENTE la información del siguiente dataset para contestar las preguntas. "
                    "Si la pregunta no está relacionada con los datos, responde con: "
                    "'Lo siento, no estoy entrenado para contestar preguntas en este ámbito.'\n\n"
                    "Aquí están los primeros 150 registros del dataset:\n" + df_string
                )
            },
            {"role": "user", "content": user_input}
        ]
    )

    # Mostrar respuesta
    answer = response.choices[0].message.content
    st.subheader("Respuesta:")
    st.write(answer)

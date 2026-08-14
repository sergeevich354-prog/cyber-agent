import streamlit as st
import requests

st.set_page_config(page_title="AI Super-Agent", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0914; color: #e0def4; }
    .stButton>button { background-color: #4c1d95; color: white; border-radius: 8px; width: 100%; border: none; height: 50px; font-size: 16px; }
    .stButton>button:hover { background-color: #6d28d9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Патрік OS v7.5 — Стратегічне Ядро")

# Твій перевірений робочий ключ Google Gemini
GEMINI_KEY = "AQ.Ab8RN6IHABjkcUUydXVQCtINDSSP439Y3pSsymlDS3YGoaZZUw"

def ask_ai(system_prompt, user_query):
    url = f"https://googleapis.com{GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\nЗапит: {user_query}"}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Помилка Google API (Код {response.status_code}): {response.text}"
    except Exception as e:
        return f"Збій з'єднання з Google: {str(e)}"

user_query = st.text_area("Введіть бізнес-ідею:", value="розчіска в Охтирці")

if st.button("⚡ Запустити стратегічне ядро"):
    sys_prompt = "Ти — видатний бізнес-аналітик. Знайди 5 прихованих загроз чому ідея провалиться в цьому місті, і як їм запобігти. Відповідай українською."
    with st.spinner("Зв'язок із серверами Google..."):
        res = ask_ai(sys_prompt, user_query)
        st.subheader("РЕЗУЛЬТАТ АНАЛІЗУ")
        st.markdown(res)

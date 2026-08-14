import streamlit as st
import requests

st.set_page_config(page_title="AI Super-Agent", layout="wide")
st.title("🤖 Патрік OS v8.5 — Стратегічне Ядро")

KEY = "AQ.Ab8RN6IHABjkcUUydXVQCtINDSSP439Y3pSsymlDS3YGoaZZUw"
# Винесли адресу на самий початок, де немає пробілів і нічого не зламається:
URL = f"https://googleapis.com{KEY}"

def ask_ai(sys_prompt, user_query):
    payload = {"contents": [{"parts": [{"text": f"{sys_prompt}\n\nЗапит: {user_query}"}]}]}
    try:
        res = requests.post(URL, headers={"Content-Type": "application/json"}, json=payload)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Помилка Google API: {res.text}"
    except Exception as e:
        return f"Збій з'єднання: {str(e)}"

query = st.text_area("Введіть бізнес-ідею:", value="розчіска в Охтирці")

if st.button("⚡ Запустити战略 ядро"):
    prompt = "Ти — видатний бізнес-аналітик. Знайди 5 прихованих загроз чому ідея провалиться в цьому місті, і як їм запобігти. Відповідай українською."
    with st.spinner("Зв'язок із серверами Google..."):
        result = ask_ai(prompt, query)
        st.subheader("РЕЗУЛЬТАТ АНАЛІЗУ")
        st.markdown(result)

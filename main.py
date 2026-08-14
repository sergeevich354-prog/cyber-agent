import streamlit as st
import requests
import os

# Налаштування сторінки кібер-дашборду
st.set_page_config(page_title="AI Super-Agent Dashboard", page_icon="🧠", layout="wide")

# Стилізація під темно-фіолетовий кіберпанк
st.markdown("""
    <style>
    .main { background-color: #0b0914; color: #e0def4; }
    .stButton>button { background-color: #4c1d95; color: white; border-radius: 8px; width: 100%; border: none; height: 50px; font-size: 16px; }
    .stButton>button:hover { background-color: #6d28d9; }
    div[data-testid="stExpander"] { background-color: #141026; border: 1px solid #4c1d95; }
    </style>
    """, unsafe_allow_html=True)

# Зашиваємо безкоштовний публічний ключ для тестів напряму
API_KEY = os.environ.get("OPENROUTER_API_KEY")

st.sidebar.title("🤖 Патрік OS v1.1")
mode = st.sidebar.selectbox("Обери модуль агента:", [
    "🧠 Кібер-Strategist", 
    "👁️ Візуальний Аудит", 
    "📱 SMM Автопілот", 
    "💻 Кухня Коду"
])

st.title(f"🤖 Модуль: {mode}")

# Офіційний прямий запит без помилок OpenRouter
def ask_ai(system_prompt, user_query):
    if not API_KEY:
        return "Помилка: Ключ не знайдено в налаштуваннях сервісу Render!"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://render.com",
        "X-Title": "Cyber Agent"
    }
    
    # Використовуємо стабільну базову модель без лімітів
    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    }
    
    try:
        response = requests.post("https://openrouter.ai", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices']['message']['content']
        else:
            return f"Сервер відповів: {response.text}"
    except Exception as e:
        return f"Збій мережі: {str(e)}"

# 1. КІБЕР-СТРАТЕГ
if mode == "🧠 Кібер-Strategist":
    user_query = st.text_area("Введіть твою бізнес-ідею або питання для аналізу аналітики:", placeholder="Наприклад: розчіска в Охтирці", value="розчіска в Охтирці")
    devils_advocate = st.checkbox("Aктивувати режим Devil's Advocate", value=True)
    
    if st.button("⚡ Запустити стратегічне ядро"):
        sys_prompt = "Ти — видатний бізнес-аналітик. Відповідай структуровано, українською мовою."
        if devils_advocate:
            sys_prompt += " Увімкни режим Devil's Advocate: знайди 5 причин чому ідея провалиться в цьому місті, і як їм запобігти."
            
        with st.spinner("Синтез аналітики..."):
            res = ask_ai(sys_prompt, user_query)
            st.subheader("РЕЗУЛЬТАТ АНАЛІЗУ")
            st.markdown(res)

# 2. ВІЗУАЛЬНИЙ АУДИТ
elif mode == "👁️ Візуальний Аудит":
    doc_desc = st.text_area("Опишіть документ чи аудит профілю:")
    if st.button("📝 Згенерувати звіт"):
        with st.spinner("Синтез..."):
            res = ask_ai("Ти — технічний асистент. Пиши українською.", doc_desc)
            st.markdown(res)

# 3. SMM АВТОПІЛОТ
elif mode == "📱 SMM Автопілот":
    niche = st.text_input("Ніша бізнесу:")
    city = st.text_input("Місто:")
    if st.button("🚀 Створити SMM-Стратегію"):
        with st.spinner("Генерація..."):
            res = ask_ai("Ти — SMM-маркетолог. Пиши тексти з гачками українською.", f"План для {niche} у {city}")
            st.markdown(res)

# 4. КУХНЯ КОДУ
elif mode == "💻 Кухня Коду":
    code_task = st.text_area("Який сайт написати?")
    if st.button("🛠️ Згенерувати код"):
        with st.spinner("Кодування..."):
            res = ask_ai("Ти — Senior Engineer. Пиши виключно чистий HTML/CSS код.", code_task)
            st.code(res)

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

# Отримуємо ключ OpenRouter
API_KEY = os.environ.get("OPENROUTER_API_KEY")

st.sidebar.title("🤖 Патрік OS v1.0")
mode = st.sidebar.selectbox("Обери модуль агента:", [
    "🧠 Кібер-Strategist", 
    "👁️ Візуальний Аудит", 
    "📱 SMM Автопілот", 
    "💻 Кухня Коду"
])

st.title(f"🤖 Модуль: {mode}")

# Функція для запиту до OpenRouter
def ask_ai(system_prompt, user_query):
    if not API_KEY:
        return "Помилка: OPENROUTER_API_KEY не знайдено в налаштуваннях сервісу!"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"OpenRouter повернув помилку {response.status_code}: {response.text}"
    except Exception as e:
        return f"Помилка з'єднання: {str(e)}"

# 1. КІБЕР-СТРАТЕГ
if mode == "🧠 Кібер-Strategist":
    user_query = st.text_area("Введіть твою бізнес-ідею або питання для аналізу аналітики:", placeholder="Наприклад: Який товар запустить в Україні цієї осені?")
    devils_advocate = st.checkbox("Активувати режим Devil's Advocate (Жорсткий стрес-тест ризиків)", value=True)

    if st.button("⚡ Запустити стратегічне ядро"):
        sys_prompt = "Ти — видатний бізнес-аналітик. Відповідай чітко, структуровано, українською мовою."
        if devils_advocate:
            sys_prompt += " Увімкни режим Devil's Advocate: знайди приховані загрози, касові розриви та причини чому ідея провалиться, і як їм запобігти."

        with st.spinner("Обробка сигналу..."):
            st.info("Підготовка контексту // openrouter/auto")
            res = ask_ai(sys_prompt, user_query)
            st.subheader("РЕЗУЛЬТАТ АНАЛІЗУ")
            st.markdown(res)

# 2. ВІЗУАЛЬНИЙ АУДИТ
elif mode == "👁️ Візуальний Аудит":
    st.info("Примітка: Локальний текстовий опис документів та фото.")
    doc_desc = st.text_area("Опишіть, який документ потрібно згенерувати або яку проблему на фото проаналізувати:")

    if st.button("📝 Згенерувати документ / Аналіз"):
        with st.spinner("Синтез тексту..."):
            res = ask_ai("Ти — юридичний та технічний асистент. Створюй повноцінні документи чи звіти за описом українською мовою.", doc_desc)
            st.markdown(res)

# 3. SMM АВТОПІЛОТ
elif mode == "📱 SMM Автопілот":
    niche = st.text_input("Ніша бізнесу (наприклад: Налаштування Google Maps, Продаж PowerStation):")
    city = st.text_input("Місто (наприклад: Охтирка, Миколаїв):")

    if st.button("🚀 Створити SMM-Стратегію"):
        query = f"Створи контент-план та скрипти продажів для ніші {niche} у місті {city}."
        with st.spinner("Генерація контенту..."):
            res = ask_ai("Ти — топ SMM-маркетолог. Пиши вірусні тексти, гачки, хештеги та скрипти для Direct/WhatsApp українською.", query)
            st.markdown(res)

# 4. КУХНЯ КОДУ
elif mode == "💻 Кухня Коду":
    code_task = st.text_area("Який сайт чи скрипт потрібно написати?", placeholder="Наприклад: Односторінковий сайт для продажу зарядних станцій на HTML/CSS з темно-фіолетовою темою.")

    if st.button("🛠️ Згенерувати чистий код"):
        with st.spinner("Кодування..."):
            res = ask_ai("Ти — Senior Full-Stack Engineer. Пиши виключно чистий, робочий код без зайвих розмов. Якщо це HTML, роби дизайн адаптивним для телефонів.", code_task)
            st.code(res)

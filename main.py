import streamlit as st
import requests

# 1. Налаштування сторінки кібер-дашборду
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

# Твій офіційний перевірений ключ Google Gemini
GEMINI_KEY = "AQ.Ab8RN6IHABjkcUUydXVQCtINDSSP439Y3pSsymlDS3YGoaZZUw"

# Чиста адреса запиту до Google API
URL = f"https://googleapis.com{GEMINI_KEY}"

st.sidebar.title("🤖 Патрік OS v9.0")
mode = st.sidebar.selectbox("Обери модуль агента:", [
    "🧠 Кібер-Strategist", 
    "👁️ Візуальний Аудит", 
    "📱 SMM Автопілот", 
    "💻 Кухня Коду"
])

st.title(f"🤖 Модуль: {mode}")

# Пряма функція запиту до Google Gemini
def ask_ai(system_prompt, user_query):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"System Instruction: {system_prompt}\n\nUser Question: {user_query}"
            }]
        }]
    }
    try:
        response = requests.post(URL, headers=headers, json=payload)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
            # return res_json['candidates']['content']['parts']['text']
        else:
            return f"Помилка Google API (Код {response.status_code}): {response.text}"
    except Exception as e:
        return f"Збій з'єднання з Google: {str(e)}"

# ——————————————————————————————————————————————————————————————————————
# 1. КІБЕР-СТРАТЕГ
# ——————————————————————————————————————————————————————————————————————
if mode == "🧠 Кібер-Strategist":
    user_query = st.text_area("Введіть твою бізнес-ідею або питання для аналізу:", placeholder="Наприклад: розчіска в Охтирці", value="розчіска в Охтирці")
    devils_advocate = st.checkbox("Активувати режим Devil's Advocate (Жорсткий стрес-тест ризиків)", value=True)
    
    if st.button("⚡ Запустити стратегічне ядро"):
        sys_prompt = "Ти — видатний бізнес-аналітик. Відповідай чітко, структуровано, виключно українською мовою."
        if devils_advocate:
            sys_prompt += " Увімкни режим Devil's Advocate: знайди приховані загрози, касові розриви та 5 причин чому ідея провалиться, і як їм запобігти."
            
        with st.spinner("Обробка сигналу Google..."):
            res = ask_ai(sys_prompt, user_query)
            st.subheader("РЕЗУЛЬТАТ АНАЛІЗУ")
            st.markdown(res)

# ——————————————————————————————————————————————————————————————————————
# 2. ВІЗУАЛЬНИЙ АУДИТ
# ——————————————————————————————————————————————————————————————————————
elif mode == "👁️ Візуальний Аудит":
    doc_desc = st.text_area("Опишіть, який документ потрібно згенерувати або яку проблему проаналізувати:")
    
    if st.button("📝 Згенерувати документ / Аналіз"):
        with st.spinner("Синтез тексту з серверів Google..."):
            res = ask_ai("Ти — юридичний та технічний асистент. Створюй повноцінні документи чи звіти за описом українською мовою.", doc_desc)
            st.subheader("ЗГЕНЕРОВАНИЙ ЗВІТ")
            st.markdown(res)

# ——————————————————————————————————————————————————————————————————————
# 3. SMM АВТОПІЛОТ
# ——————————————————————————————————————————————————————————————————————
elif mode == "📱 SMM Автопілот":
    niche = st.text_input("Ніша бізнесу (наприклад: Продаж розчісок):", value="Продаж розчісок")
    city = st.text_input("Місто (наприклад: Охтирка):", value="Охтирка")
    
    if st.button("🚀 Створити SMM-Стратегію"):
        query = f"Створи контент-план та скрипти продажів для ніші {niche} у місті {city}."
        with st.spinner("Генерація контенту..."):
            res = ask_ai("Ти — топ SMM-маркетолог. Пиши вірусні тексти, гачки, хештеги та скрипти для Direct/WhatsApp українською.", query)
            st.subheader("SMM КОНТЕНТ-ПЛАН")
            st.markdown(res)

# ——————————————————————————————————————————————————————————————————————
# 4. КУХНЯ КОДУ
# ——————————————————————————————————————————————————————————————————————
elif mode == "💻 Кухня Коду":
    code_task = st.text_area("Який сайт чи скрипт потрібно написати?", placeholder="Наприклад: Односторінковий сайт для продажу на HTML/CSS з темно-фіолетовою темою.")
    
    if st.button("🛠️ Згенерувати чистий код"):
        with st.spinner("Кодування..."):
            res = ask_ai("Ти — Senior Full-Stack Engineer. Пиши виключно чистий, робочий код без зайвих розмов. Якщо це HTML, роби дизайн адаптивним для телефонів.", code_task)
            st.subheader("ЗГЕНЕРОВАНИЙ КОД")
            st.code(res)

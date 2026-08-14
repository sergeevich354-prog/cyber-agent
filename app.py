import base64
import io
import mimetypes
import os
import zipfile
from datetime import datetime
from html import escape
from typing import Any
from xml.etree import ElementTree

import requests
import streamlit as st


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_OPTIONS = {
    "Gemini Flash 1.5 8B": "google/gemini-flash-1.5-8b:free",
    "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct:free",
}


st.set_page_config(
    page_title="NEXUS // AI Super-Agent",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
          --ink: #f4f0ff;
          --muted: #9d96b8;
          --violet: #a970ff;
          --hot: #ed67ff;
          --cyan: #52e5ff;
          --panel: rgba(28, 20, 51, .78);
          --line: rgba(177, 126, 255, .22);
        }
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
        .stApp {
          background:
            radial-gradient(circle at 88% 4%, rgba(133, 53, 255, .24), transparent 28rem),
            radial-gradient(circle at 0% 46%, rgba(34, 133, 214, .10), transparent 22rem),
            #090711;
          color: var(--ink);
        }
        .stApp::before {
          content: "";
          position: fixed; inset: 0; pointer-events: none; opacity: .17; z-index: 0;
          background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
          background-size: 28px 28px;
          mask-image: linear-gradient(to bottom, black, transparent 90%);
        }
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #120d22 0%, #0d0919 100%);
          border-right: 1px solid var(--line);
        }
        section[data-testid="stSidebar"] > div { padding-top: 1.1rem; }
        .block-container { max-width: 920px; padding: 2.1rem 1.15rem 4rem; }
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.04em; }
        h1 { font-size: clamp(2rem, 8vw, 3.7rem) !important; line-height: .98 !important; }
        h2 { font-size: clamp(1.45rem, 6vw, 2.3rem) !important; }
        .brand {
          display: flex; align-items: center; gap: .65rem; margin: .2rem 0 2rem;
          font-family: 'DM Mono', monospace; font-size: .82rem; letter-spacing: .1em;
          color: #d7c4ff;
        }
        .brand-mark {
          display: grid; place-items: center; width: 2.25rem; height: 2.25rem;
          border: 1px solid var(--violet); border-radius: .65rem;
          color: var(--cyan); box-shadow: 0 0 22px rgba(169,112,255,.42);
          background: rgba(169,112,255,.14); font-size: 1.1rem;
        }
        .eyebrow {
          font-family: 'DM Mono', monospace; font-size: .69rem; letter-spacing: .16em;
          text-transform: uppercase; color: var(--cyan); margin-bottom: .8rem;
        }
        .hero-copy { max-width: 45rem; color: var(--muted); font-size: 1rem; line-height: 1.6; }
        .hero-copy strong { color: var(--ink); font-weight: 500; }
        .status-strip {
          display: flex; flex-wrap: wrap; gap: .55rem; margin: 1.25rem 0 1.7rem;
        }
        .status-pill {
          display: inline-flex; align-items: center; gap: .45rem; padding: .42rem .65rem;
          border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.035);
          color: #cfc5e8; font: .68rem 'DM Mono', monospace; letter-spacing: .04em;
        }
        .status-dot { width: .4rem; height: .4rem; border-radius: 50%; background: #62ffba; box-shadow: 0 0 10px #62ffba; }
        .panel {
          position: relative; border: 1px solid var(--line); background: var(--panel);
          border-radius: 1.1rem; padding: 1.15rem; margin: 1rem 0;
          box-shadow: 0 18px 55px rgba(0,0,0,.22);
        }
        .panel::after {
          content: ""; position: absolute; top: -1px; right: 1.25rem; width: 3.5rem; height: 1px;
          background: var(--cyan); box-shadow: 0 0 12px var(--cyan);
        }
        .panel-label {
          color: #c0b3da; font: .7rem 'DM Mono', monospace; letter-spacing: .13em;
          text-transform: uppercase; margin-bottom: .7rem;
        }
        .thinking-log {
          border-left: 1px solid rgba(82,229,255,.38); padding: .2rem 0 .2rem .75rem;
          margin: .4rem 0; color: var(--muted); font: .73rem 'DM Mono', monospace; line-height: 1.7;
        }
        .thinking-log .active { color: var(--cyan); }
        .thinking-log .done { color: #bbb0d3; }
        .thinking-log .time { color: #615879; margin-right: .4rem; }
        .output-shell {
          border: 1px solid rgba(169,112,255,.28); border-radius: .9rem;
          padding: .2rem .85rem; background: rgba(7,5,16,.5);
        }
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
          background: rgba(5,4,14,.7) !important; border: 1px solid rgba(177,126,255,.29) !important;
          color: var(--ink) !important; border-radius: .75rem !important;
        }
        [data-testid="stFileUploader"] section {
          background: rgba(5,4,14,.45); border: 1px dashed rgba(169,112,255,.48);
          border-radius: .85rem;
        }
        .stButton > button, .stDownloadButton > button {
          width: 100%; border: 1px solid rgba(169,112,255,.55); border-radius: .72rem;
          min-height: 2.8rem; background: linear-gradient(110deg, rgba(121,57,204,.82), rgba(60,44,125,.9));
          color: white; font-weight: 600; transition: all .2s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
          border-color: var(--cyan); box-shadow: 0 0 20px rgba(82,229,255,.16);
          transform: translateY(-1px);
        }
        .stCheckbox label, .stRadio label, .stMultiSelect label, .stSelectbox label,
        .stTextInput label, .stTextArea label, .stFileUploader label { color: #d8d0e7 !important; }
        div[data-baseweb="tab-list"] { gap: .3rem; }
        button[data-baseweb="tab"] { color: #a79cbd; }
        button[data-baseweb="tab"][aria-selected="true"] { color: var(--cyan); }
        .stMarkdown, .stAlert { line-height: 1.65; }
        [data-testid="stMetricValue"] { color: var(--cyan); }
        @media (max-width: 640px) {
          .block-container { padding: 1.35rem .85rem 3rem; }
          section[data-testid="stSidebar"] { min-width: 82vw; max-width: 88vw; }
          .panel { padding: .92rem; border-radius: .9rem; }
          .hero-copy { font-size: .93rem; }
          .stButton > button { min-height: 3.1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "thinking_log" not in st.session_state:
        st.session_state.thinking_log = []
    if "last_output" not in st.session_state:
        st.session_state.last_output = ""


def add_log(message: str, state: str = "done") -> None:
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.thinking_log.append({"time": now, "message": message, "state": state})
    st.session_state.thinking_log = st.session_state.thinking_log[-8:]


def render_thinking_log() -> None:
    rows = st.session_state.get("thinking_log", [])
    if not rows:
        rows = [{"time": "--:--:--", "message": "Ядро очікує на команду…", "state": "active"}]
    html = "".join(
        f'<div class="{row["state"]}"><span class="time">{row["time"]}</span>{escape(row["message"])}</div>'
        for row in rows
    )
    st.markdown(f'<div class="thinking-log">{html}</div>', unsafe_allow_html=True)


def model_choice() -> str:
    selected_name = st.selectbox(
        "Модель OpenRouter",
        list(MODEL_OPTIONS.keys()),
        format_func=lambda value: value,
        key="model_selector",
    )
    # Keep friendly names in the UI, but return the exact OpenRouter model ID.
    return MODEL_OPTIONS[selected_name]


def call_openrouter(
    prompt: str,
    model: str,
    *,
    image_payload: dict[str, Any] | None = None,
    temperature: float = 0.7,
) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY не налаштовано.")

    if image_payload:
        user_content: Any = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_payload["data_url"]}},
        ]
    else:
        user_content = prompt

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://replit.com",
            "X-Title": "NEXUS AI Super-Agent Dashboard",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ти — NEXUS, українськомовний AI Super-Agent. "
                        "Відповідай чистою українською мовою у структурованому Markdown. "
                        "Не вигадуй факти, чітко позначай припущення. "
                        "Пиши змістовно, але без зайвої води."
                    ),
                },
                {"role": "user", "content": user_content},
            ],
            "temperature": temperature,
            "max_tokens": 2400,
        },
        timeout=90,
    )
    if response.status_code >= 400:
        detail = response.text[:500]
        raise RuntimeError(f"OpenRouter повернув помилку {response.status_code}: {detail}")
    body = response.json()
    choices = body.get("choices", [])
    if not choices:
        raise RuntimeError("Модель не повернула текстову відповідь.")
    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        content = "\n".join(item.get("text", "") for item in content if isinstance(item, dict))
    return str(content).strip()


def extract_file_text(uploaded_file: Any) -> str:
    data = uploaded_file.getvalue()
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1] if "." in uploaded_file.name else ""
    if suffix in {"txt", "md", "csv", "json", "py", "html", "css", "js"}:
        return data.decode("utf-8", errors="replace")[:18000]
    if suffix == "pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(data))
            return "\n\n".join(page.extract_text() or "" for page in reader.pages)[:18000]
        except Exception as exc:
            return f"[Не вдалося витягти PDF як текст: {exc}]"
    if suffix == "docx":
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                xml = archive.read("word/document.xml")
            root = ElementTree.fromstring(xml)
            text = " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))
            return text[:18000]
        except Exception as exc:
            return f"[Не вдалося витягти DOCX як текст: {exc}]"
    return ""


def file_image_payload(uploaded_file: Any) -> dict[str, str] | None:
    mime = uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0] or ""
    if not mime.startswith("image/"):
        return None
    encoded = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
    return {"data_url": f"data:{mime};base64,{encoded}"}


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            '<div class="brand"><div class="brand-mark">✦</div><div>NEXUS<br><span style="color:#6e6687">SUPER-AGENT / 01</span></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="panel-label">Навігація системи</div>', unsafe_allow_html=True)
        section = st.radio(
            "Модулі",
            [
                "🧠 Cyber-Strategist",
                "👁️ Vision & Documents",
                "📱 SMM Autopilot",
                "💻 Code Kitchen",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown('<div class="panel-label">Стан ядра</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="status-pill"><span class="status-dot"></span> OPENROUTER ONLINE</div>',
            unsafe_allow_html=True,
        )
        st.caption("Моделі працюють через захищений проксі OpenRouter.")
        if st.button("Очистити журнал", use_container_width=True):
            st.session_state.thinking_log = []
            st.rerun()
    return section


def page_header(kicker: str, title: str, description: str) -> None:
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="hero-copy">{description}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="status-strip"><span class="status-pill"><span class="status-dot"></span> СИСТЕМА ГОТОВА</span><span class="status-pill">UA // MARKDOWN</span><span class="status-pill">MOBILE OPTIMIZED</span></div>',
        unsafe_allow_html=True,
    )


def strategist_page() -> None:
    page_header(
        "NEXUS / CORE",
        "Думай глибше.",
        "Стратегічне AI‑ядро для рішень, планів і розбору складних задач. Додай контекст — я розкладу проблему по шарах.",
    )
    with st.container(border=True):
        st.markdown('<div class="panel-label">Вхідний сигнал</div>', unsafe_allow_html=True)
        prompt = st.text_area(
            "Що потрібно вирішити?",
            placeholder="Наприклад: як запустити продукт на українському ринку за 30 днів?",
            height=150,
            label_visibility="collapsed",
        )
        col1, col2 = st.columns(2)
        with col1:
            model = model_choice()
        with col2:
            devil = st.checkbox("Devil's Advocate", help="Додасть окремий стрес-тест плану: ризики, контраргументи та слабкі місця.")
        if st.button("⚡ Запустити стратегічне ядро", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Додай задачу або питання для аналізу.")
            else:
                add_log("Отримано новий стратегічний сигнал", "active")
                add_log(f"Підготовка контексту // {model}", "active")
                if devil:
                    add_log("Активовано режим Devil's Advocate", "active")
                render_thinking_log()
                instruction = (
                    f"Проаналізуй запит користувача: {prompt}\n\n"
                    "Побудуй відповідь у Markdown зі структурами: ## Короткий висновок, "
                    "## Глибокий аналіз, ## План дій, ## Метрики успіху. "
                    "Якщо даних недостатньо — сформулюй до 3 уточнень."
                )
                if devil:
                    instruction += (
                        "\n\nДодай блок ## Devil's Advocate: атакуй власну рекомендацію, "
                        "назви 5 ризиків, контраргументи й конкретні запобіжники."
                    )
                try:
                    result = call_openrouter(instruction, model)
                    st.session_state.last_output = result
                    add_log("Відповідь синтезовано", "done")
                except Exception as exc:
                    add_log("Синхронізація з моделлю перервана", "done")
                    st.error(str(exc))
    with st.expander("◉ LIVE THINKING LOG", expanded=True):
        render_thinking_log()
    if st.session_state.last_output:
        st.markdown('<div class="panel-label">Результат аналізу</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-shell">{st.session_state.last_output}</div>', unsafe_allow_html=True)


def vision_page() -> None:
    page_header(
        "NEXUS / SIGHT",
        "Побачити більше.",
        "Завантаж зображення або документ для розбору. Або опиши майбутній документ — ядро створить готовий текст українською.",
    )
    mode = st.radio("Режим", ["Аналіз файлу", "Створити текстовий документ"], horizontal=True)
    if mode == "Аналіз файлу":
        uploaded = st.file_uploader("Файл для аналізу", type=["png", "jpg", "jpeg", "webp", "pdf", "docx", "txt", "md", "csv", "json"])
        if uploaded:
            st.caption(f"Підключено: **{uploaded.name}** · {uploaded.size / 1024:.1f} KB")
            question = st.text_area(
                "Фокус аналізу",
                placeholder="Що саме знайти, пояснити або перевірити в цьому файлі?",
                height=100,
            )
            model = model_choice()
            if st.button("👁️ Проаналізувати файл", type="primary", use_container_width=True):
                add_log(f"Файл підключено // {uploaded.name}", "active")
                add_log("Виділення тексту та візуальних сигналів", "active")
                text = extract_file_text(uploaded)
                image = file_image_payload(uploaded)
                context = (
                    f"Користувацький фокус: {question or 'зроби повний структурований аналіз'}\n"
                    f"Назва файлу: {uploaded.name}\n"
                )
                if text:
                    context += f"\nТекстовий вміст:\n{text}"
                if image:
                    context += "\nЦе зображення. Розпізнай текст, об'єкти, композицію, дані та важливі деталі."
                if not text and not image:
                    context += "\nФормат не підтримує прямий аналіз. Поясни це й запропонуй конвертувати файл у PDF, DOCX або зображення."
                try:
                    result = call_openrouter(
                        context
                        + "\n\nВідповідь у Markdown: ## Виявлено, ## Детальний розбір, ## Наступні кроки.",
                        model,
                        image_payload=image,
                    )
                    st.session_state.last_output = result
                    add_log("Візуальний / документальний аналіз завершено", "done")
                except Exception as exc:
                    st.error(str(exc))
    else:
        description = st.text_area(
            "Опиши документ",
            placeholder="Створи короткий бриф для запуску кампанії кав'ярні: ціль, аудиторія, тон і 5 ключових повідомлень.",
            height=180,
        )
        doc_type = st.selectbox("Тип документа", ["Бриф", "Звіт", "Лист", "Інструкція", "Контент-план", "Власний формат"])
        model = model_choice()
        if st.button("✦ Згенерувати документ", type="primary", use_container_width=True):
            if not description.strip():
                st.warning("Додай опис документа.")
            else:
                add_log("Формуємо структуру документа", "active")
                try:
                    result = call_openrouter(
                        f"Створи {doc_type.lower()} на основі опису:\n{description}\n\n"
                        "Дай готовий до копіювання документ у чистому українському Markdown. "
                        "Додай заголовки, списки й чіткі формулювання.",
                        model,
                    )
                    st.session_state.last_output = result
                    add_log("Документ готовий до експорту", "done")
                except Exception as exc:
                    st.error(str(exc))
    if st.session_state.last_output:
        st.markdown('<div class="panel-label">Вихідний документ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-shell">{st.session_state.last_output}</div>', unsafe_allow_html=True)
        st.download_button("↓ Завантажити як Markdown", st.session_state.last_output, "nexus-document.md", "text/markdown", use_container_width=True)


def smm_page() -> None:
    page_header(
        "NEXUS / SIGNAL",
        "Автопілот контенту.",
        "Перетвори тренд або бізнес‑ціль на контент, який хочеться зберегти, переслати й обговорити.",
    )
    tab_plan, tab_replies = st.tabs(["Контент-план", "Prompt Builder"])
    with tab_plan:
        with st.container(border=True):
            trend = st.text_area("Тренд або тема", placeholder="Наприклад: локальні бренди, slow living, AI для малого бізнесу", height=110)
            col1, col2 = st.columns(2)
            with col1:
                platform = st.multiselect("Канали", ["Instagram", "WhatsApp"], default=["Instagram", "WhatsApp"])
            with col2:
                days = st.slider("Днів контенту", 3, 14, 7)
            audience = st.text_input("Аудиторія", placeholder="Хто має це читати?")
            model = model_choice()
            if st.button("📱 Зібрати SMM-план", type="primary", use_container_width=True):
                if not trend.strip():
                    st.warning("Вкажи тренд або тему.")
                else:
                    add_log("Скануємо контентний сигнал", "active")
                    try:
                        result = call_openrouter(
                            f"Побудуй контент-план на {days} днів для {', '.join(platform) or 'Instagram'}.\n"
                            f"Тема/тренд: {trend}\nАудиторія: {audience or 'широка українська аудиторія'}\n\n"
                            "Для кожного дня дай: назву, формат, сильний hook на перші 2 секунди, "
                            "текст поста або сценарій, CTA і 5-8 релевантних хештегів. "
                            "Окремо врахуй різницю Instagram і WhatsApp. Відповідай Markdown-таблицею.",
                            model,
                        )
                        st.session_state.last_output = result
                        add_log("Контентний маршрут побудовано", "done")
                    except Exception as exc:
                        st.error(str(exc))
    with tab_replies:
        with st.container(border=True):
            context = st.text_area("Контекст бренду", placeholder="Що продаємо, тон спілкування, правила й табу…", height=115)
            incoming = st.text_area("Повідомлення клієнта", placeholder="Встав сюди повідомлення, на яке потрібна відповідь…", height=115)
            model = model_choice()
            if st.button("↗ Створити prompt для відповіді", type="primary", use_container_width=True):
                if not incoming.strip():
                    st.warning("Додай повідомлення клієнта.")
                else:
                    add_log("Будуємо сценарій автоматичної відповіді", "active")
                    try:
                        result = call_openrouter(
                            f"Створи універсальний prompt для AI-оператора, який відповідатиме клієнту.\n"
                            f"Контекст бренду: {context or 'не вказано'}\n"
                            f"Повідомлення клієнта: {incoming}\n\n"
                            "Prompt має містити роль, правила тону, заборони, формат JSON-відповіді "
                            "з полями reply, intent, escalation та готовий приклад відповіді українською.",
                            model,
                        )
                        st.session_state.last_output = result
                        add_log("Prompt Builder завершив роботу", "done")
                    except Exception as exc:
                        st.error(str(exc))
    if st.session_state.last_output:
        st.markdown('<div class="panel-label">SMM output</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-shell">{st.session_state.last_output}</div>', unsafe_allow_html=True)


def code_page() -> None:
    page_header(
        "NEXUS / FORGE",
        "Код без шуму.",
        "Опиши результат — я зберу чистий Python або веб‑код, який можна одразу скопіювати, запустити й розвивати.",
    )
    with st.container(border=True):
        language = st.radio("Мова", ["Python", "Web"], horizontal=True)
        prompt = st.text_area(
            "Що побудувати?",
            placeholder="Наприклад: Streamlit-віджет для перевірки CSV, який показує пропуски й дублікати.",
            height=140,
        )
        constraints = st.text_input("Обмеження або стек", placeholder="Наприклад: без зовнішніх бібліотек / React + CSS / додай обробку помилок")
        model = model_choice()
        if st.button("💻 Зварити код", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Опиши, який код потрібен.")
            else:
                add_log(f"Готуємо {language}-рішення", "active")
                target = "Python" if language == "Python" else "HTML/CSS/JavaScript"
                try:
                    result = call_openrouter(
                        f"Напиши production-ready {target} код для задачі:\n{prompt}\n"
                        f"Обмеження: {constraints or 'немає'}\n\n"
                        "Поверни спочатку один fenced code block без вкладених fenced-блоків, "
                        "потім короткий Markdown-блок ## Як запустити українською. "
                        "Код має бути повним, чистим, з обробкою помилок і без Telegram Bot API.",
                        model,
                        temperature=0.35,
                    )
                    st.session_state.last_output = result
                    add_log("Код скомпільовано в робочий рецепт", "done")
                except Exception as exc:
                    st.error(str(exc))
    if st.session_state.last_output:
        st.markdown('<div class="panel-label">Generated artifact // натисни іконку копіювання</div>', unsafe_allow_html=True)
        st.code(st.session_state.last_output, language="python" if language == "Python" else "html")
        st.download_button("↓ Завантажити результат", st.session_state.last_output, "nexus-generated-code.txt", use_container_width=True)


def main() -> None:
    init_state()
    inject_styles()
    section = render_sidebar()
    if section == "🧠 Cyber-Strategist":
        strategist_page()
    elif section == "👁️ Vision & Documents":
        vision_page()
    elif section == "📱 SMM Autopilot":
        smm_page()
    else:
        code_page()


if __name__ == "__main__":
    main()
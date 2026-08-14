# NEXUS AI Super-Agent Dashboard

Мобільний Streamlit-дашборд із чотирма AI-модулями для стратегічного аналізу, роботи з файлами, SMM-контенту та генерації коду.

## Run & Operate

- `streamlit run app.py --server.port 5000` — запуск дашборда
- `python -m py_compile app.py` — швидка перевірка синтаксису
- `OPENROUTER_API_KEY` — секрет для AI-запитів через OpenRouter

## Стек

- Python 3.13, Streamlit
- OpenRouter Chat Completions API
- `requests` для HTTP-запитів
- `pypdf` і вбудований DOCX/XML парсер для документів

## Де що знаходиться

- `app.py` — єдиний Streamlit-додаток і всі чотири функціональні модулі
- `.streamlit/config.toml` — темна тема та параметри сервера
- `requirements.txt` / `pyproject.toml` — Python-залежності

## Архітектурні рішення

- OpenRouter викликається напряму зі Streamlit через `OPENROUTER_API_KEY`; ключ ніколи не виводиться в UI.
- Зображення передаються моделі як data URL, текстові формати витягуються локально перед аналізом.
- Один журнал у session state дає спільний live-статус дій між модулями.
- Інтерфейс свідомо зібраний на стандартних Streamlit-компонентах із мобільним CSS-шаром.

## Продукт

- Cyber-Strategist: структурований аналіз і режим Devil's Advocate.
- Vision & Documents: аналіз зображень/PDF/DOCX/текстів і створення Markdown-документів.
- SMM Autopilot: контент-плани для Instagram/WhatsApp і prompt builder для автовідповідей.
- Code Kitchen: генерація Python або web-коду з вбудованим копіюванням через `st.code`.

## Налаштування користувача

- Темна purple cyberpunk естетика.
- Основний UI і AI-вивід — українською мовою.
- Пріоритет — зручність на смартфоні та великі touch-цілі.

## Важливо

- Не запускати старий API-сервер як основний preview: головний процес — workflow `Start application`.
- Для візуального аналізу потрібна модель OpenRouter із підтримкою vision; для текстових файлів доступні обидві моделі.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details

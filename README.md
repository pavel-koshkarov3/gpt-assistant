 Нейро-сотрудник

# GPT Assistant на LangChain

Этот проект использует OpenAI API и LangChain для создания нейро-сотрудников, способных анализировать документы и отвечать на вопросы. Поддерживается работа с Google Docs и ChromaDB для векторного поиска.

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/gpt-assistant.git
   cd gpt-assistant
2. **Создайте виртуальное окружение и активируйте его:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   venv\Scripts\activate  # Для Windows
   ```
3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Создайте файл `.env` и добавьте API-ключи:**
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=https://api.vsegpt.ru/v1
   ```
5. **Запустите скрипт:**
   ```sh
   python main.py
   ```

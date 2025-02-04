import openai
import gradio as gr
import os
import re
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Устанавливаем кастомный API-ключ и URL для OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Получаем ключ API из переменной среды
openai.api_base = os.getenv("OPENAI_BASE_URL")  # Получаем кастомный URL из переменной среды

class GPT:
    def __init__(self, model_name):
        self.model_name = model_name
        self.log = ""
    
    def load_search_indexes(self, doc_url):
        """Загрузка документа и создание индекса для поиска"""
        try:
            # В реальном приложении здесь может быть код для загрузки документа
            self.log = f"Документ по ссылке {doc_url} загружен."
        except Exception as e:
            self.log = f"Ошибка при загрузке документа: {str(e)}"
    
    def answer_index(self, prompt, query):
        """Ответ на запрос с использованием OpenAI API"""
        try:
            # Используем OpenAI для генерации ответа (замените на свой метод для генерации ответа)
            response = openai.ChatCompletion.create(
                model=self.model_name,  # Выбираем модель
                messages=[  # Используем формат сообщений
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,  # Максимальное количество токенов в ответе
                n=1,  # Количество вариантов ответа
                stop=None,  # Стоп-символы (опционально)
                temperature=0.7  # Температура генерации
            )
            return response['choices'][0]['message']['content'].strip()  # Возвращаем текст ответа
        except Exception as e:
            return f"Ошибка при запросе: {str(e)}"

# Список моделей
models = [
    {
        "doc": "https://docs.google.com/document/d/1zvp3U-67NAoDWETNiHaMhKk6c7yuN-xMT0QUZhCy_38/edit?usp=sharing",
        "prompt": '''Ты психолог. Твоя задача — слушать пользователя, давать практичные советы и помогать найти баланс в жизни, используя методы эмоциональной поддержки, самопомощи и управления стрессом. 
                    Ты помогаешь людям справляться с тревожностью, депрессией, выгоранием, проблемами в личных отношениях и другими психологическими трудностями.
                    Ответь на запросы пользователя, предоставляя поддержку и рекомендации по темам, связанным с их эмоциональным состоянием и саморазвитием.
                    Документ с информацией для ответа на запросы: ''',
        "name": "Нейро-психолог",
        "query": "Как справиться с тревожностью?"
    },
    {
        "doc": "https://docs.google.com/document/d/1IqGa92RlFiCJvBH7TBKhPpODpru2-RDro8qiVEzoAuA/edit",
        "prompt": '''Ты менеджер контроля качества, твоя задача анализировать диалоги менеджеров по продажам с клиентами и готовить отчеты.
                    Компания продает курсы по машинному обучению.
                    Перед тобой текст диалога сделанный с помощью распознавания речи из записи zoom презентации.
                    Из-за машинного распознавания речи, в тексте могут быть ошибки распознавания, учитывая это.
                    Твоя задача делать отчеты по данному диалогу по запросам пользователя.
                    Составляй вопросы максимально точно по диалогу, не придумывай ничего от себя.
                    Текст диалога: ''',
        "name": "Нейро-менеджер контроля качества (Оценка качества по диалогу)",
        "query": "Напиши отчет, какие были потребности названы клиентом"
    }
]

# Объявляем экземпляр класса GPT
gpt = GPT("gpt-3.5-turbo")

# Gradio интерфейс
blocks = gr.Blocks()

# Работаем с блоком
with blocks as demo:
    # Объявляем элемент выбор из списка
    subject = gr.Dropdown([(elem["name"], index) for index, elem in enumerate(models)], label="Выберите модель")
    
    # Выводим выбранное имя
    name = gr.Label(show_label=False)
    
    # Промпт для запроса к LLM
    prompt = gr.Textbox(label="Промпт", interactive=True)
    
    # Ссылка на файл обучения
    link = gr.HTML()
    
    # Поле пользовательского запроса к LLM
    query = gr.Textbox(label="Запрос к модели", interactive=True)

    # Функция на выбор нейро-сотрудника в models
    def onchange(dropdown):
        return [
            models[dropdown]['name'],  # имя
            re.sub('\t+|\s\s+', ' ', models[dropdown]['prompt']),  # очищаем лишние пробелы и табуляции
            models[dropdown]['query'],  # стандартный запрос
            f"<a target='_blank' href = '{models[dropdown]['doc']}'>Документ для обучения</a>"  # ссылка на документ
        ]

    # При изменении значения в поле списка subject, вызывается функция onchange
    subject.change(onchange, inputs=[subject], outputs=[name, prompt, query, link])

    # Строка с кнопками
    with gr.Row():
        train_btn = gr.Button("Обучить модель")
        request_btn = gr.Button("Запрос к модели")

    # Функция обучения
    def train(dropdown):
        try:
            # Загрузка документа
            gpt.load_search_indexes(models[dropdown]['doc'])
            return gpt.log  # Лог выполнения
        except Exception as e:
            return f"Ошибка при обучении: {str(e)}"

    # Функция для отправки запроса
    def predict(p, q):
        try:
            result = gpt.answer_index(p, q)
            return [result, gpt.log]
        except Exception as e:
            return [f"Ошибка при запросе: {str(e)}", gpt.log]

    # Выводим поля response с ответом от LLM и log (вывод сообщений работы класса GPT) на 2 колонки
    with gr.Row():
        response = gr.Textbox(label="Ответ модели")
        log = gr.Textbox(label="Логирование")

    # Кнопка "Обучить модель"
    train_btn.click(train, inputs=[subject], outputs=log)

    # Кнопка "Запрос к модели"
    request_btn.click(predict, inputs=[prompt, query], outputs=[response, log])

# Запуск приложения
demo.launch()

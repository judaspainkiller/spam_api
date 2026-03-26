from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import re
import nltk 
import string 
from nltk.stem import WordNetLemmatizer
import pandas as pd

nltk.download('wordnet')
nltk.download('omw-1.4')

# 1. Загружаем модель
with open('spam_classifier_rf.pkl', 'rb') as f:
    data = pickle.load(f)
    model = data['model']
    vectorizer = data['vectorizer']

# 2. Создаем FastAPI приложение
app = FastAPI(title="Spam Detector API", description="Определяет, является ли сообщение спамом")
   
# class Task(BaseModel):
#     name: str
#     description: str | None = None

#3. Определяем формат входных данных
class Item(BaseModel):
    text: str

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    # Удаление пунктуации
    text = re.sub(f'[{string.punctuation}]', '', text)
    # Удаление цифр
    text = re.sub(r'\d+', '', text)
    # Удаление лишних пробелов
    text = re.sub(r'\s+', ' ', text).strip()
    # Токенизация
    tokens = text.split()
    # Лемматизация
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Эндпоинт для проверки работы сервера
@app.get("/")
def root():
    return {"message": "Spam Detector API is running"}

# 4. Эндпоинт для предсказания
@app.post("/predict")
def predict(item: Item):
    # Здесь предобработка текста
    try:
        processed_text = preprocess_text(item.text)
        if not processed_text:
            return {
                "text" : item.text,
                "prediction" : 0,
                "probability" : None,
                "message" : "Текст пустой или не содержит значимой информации"
            }
        features = vectorizer.transform([processed_text])
        prediction = model.predict(features)[0]
        # prediction = model.predict([processed_text])[0]
        
        return {
            "text": item.text,
            "is_spam": bool(prediction),
            "result": "спам" if prediction else "не спам"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при предсказании: {str(e)}")

# 5. Эндпоинт для информации о модели
@app.get("/info")
def get_info():
    return {
        "model_type": type(model).__name__,
        "description": "Модель для определения спама в текстовых сообщениях",
        "preprocessing": "lowercase, punctuation removal, digit removal, tokenization, lemmatization"
    }

# class STaskAdd(BaseModel):
#     name: str
#     desciption: str | None = None

# class Task(STaskAdd):
#     id: int

# tasks = []

# # вот этот блок работает
# @app.get("/home")
# def get_home():
#     return {"data": "Hello, World!"}

# @app.get("/tasks")
# def get_tasks():
#     task = Task(name="не сторчаться")
#     return {"data": task}

# вот эти два нет 

# @app.post("/tasks")
# async def add_task(
#     task: Annotated[STaskAdd, Depends()]
#     ):
#     tasks.append(task)
#     return {"ok": True}


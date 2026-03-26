# Проект с разработкой модели для классификации спама с использованием API и Docker

API для определения спама в текстовых сообщениях на русском языке. Модель обучена на основе Random Forest с использованием TF-IDF векторизации.

## 📊 Метрики модели
- Accuracy: 91%
- ROC-AUC: 97%

## 🛠 Технологии
- Python 3.11
- FastAPI
- scikit-learn
- NLTK
- Docker

## 🚀 Запуск

### Локально
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Для обучения использован следующий датасет с сайта HuggingFace: hf://datasets/DmitryKRX/anti_spam_ru/df.csv 

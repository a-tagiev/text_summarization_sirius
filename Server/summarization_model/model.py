import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import os.path
import pickle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

pipe = pipeline("summarization", model="d0rj/rut5-base-summ")

nltk.download('punkt')
nltk.download('stopwords')

with open(f"{BASE_DIR}/pretrained_model.pkl", "rb") as f:
    model = pickle.load(f)


def summarize_text_abstract(text):
    out = pipe(text, min_length=10, max_length=300, length_penalty=5)[0]['summary_text']
    return out


def summarize_text_extract(text, num_sentences=3):
    # Разделение текста на предложения
    sentences = sent_tokenize(text)

    # Подготовка списка стоп-слов для удаления из текста
    stop_words = set(stopwords.words('russian'))

    # Подготовка частотного словаря для слов
    word_freq = defaultdict(int)

    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if word not in stop_words:
                word_freq[word] += 1

    # Оценка важности предложений на основе суммы частот слов в них
    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence.lower())
        for word in words:
            if word in word_freq:
                sentence_scores[i] += word_freq[word]

    # Выбор наиболее важных предложений
    selected_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    # Составление суммаризации на основе выбранных предложений
    summary = [sentences[j] for j in sorted(selected_sentences)]
    return ' '.join(summary)


def tonality_predict(text):
    pred = model.predict(text)
    if pred[0]["label"].lower() == "neutral":
        return "Нейтральный &#128566;"
    elif pred[0]["label"].lower() == "positive":
        return "Позитивный &#129409;"
    return "Негативный &#129313;"


import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
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
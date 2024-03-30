import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest
from transformers import pipeline
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text):
    pipe = pipeline("summarization", model="sarahai/ruT5-base-summarizer",tokenizer=tokenizer)
    return pipe(text,min_length=5, max_length=100)[0]['summary_text']

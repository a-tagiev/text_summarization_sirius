import os.path
import pickle


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


with open(f"{BASE_DIR}/pretrained_model.pkl", "rb") as f:
    model = pickle.load(f)


def tonality_predict(text):
    pred = model.predict(text)
    if pred[0]["label"].lower() == "neutral":
        return "Нейтральный &#128566;"
    elif pred[0]["label"].lower() == "positive":
        return "Позитивный &#129409;"
    return "Негативный &#129313;"
import os.path
import pickle


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


with open(f"{BASE_DIR}/best_model.pkl", "rb") as f:
    model = pickle.load(f)


def tonality_predict(text):
    pred = model.predict(text)
    return pred[0]
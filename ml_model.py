import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

DATA_PATH = "data/Training.csv"

df = pd.read_csv(DATA_PATH)
df.fillna(0, inplace=True)

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

le = LabelEncoder()
y = le.fit_transform(y)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

ALL_SYMPTOMS = list(X.columns)


def normalize_symptoms(text):
    text = text.lower()
    text = text.replace(",", " ")
    words = text.split()
    matched = []

    for s in ALL_SYMPTOMS:
        for w in words:
            if w in s.replace("_", " "):
                matched.append(s)
    return list(set(matched))


def predict_disease(symptom_text):
    matched_symptoms = normalize_symptoms(symptom_text)

    if not matched_symptoms:
        return None, None, None

    input_data = np.zeros(len(ALL_SYMPTOMS))
    for s in matched_symptoms:
        input_data[ALL_SYMPTOMS.index(s)] = 1

    probs = model.predict_proba([input_data])[0]
    top_indices = np.argsort(probs)[::-1][:4]

    main_disease = le.inverse_transform([top_indices[0]])[0]
    confidence = round(probs[top_indices[0]] * 100, 2)

    other_diseases = [
        le.inverse_transform([i])[0] for i in top_indices[1:]
    ]

    return main_disease, confidence, other_diseases

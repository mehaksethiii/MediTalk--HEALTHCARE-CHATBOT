from ml_model import predict_disease
from precautions import PRECAUTIONS

COMMON_DISEASES = [
    "Common Cold",
    "Viral Fever",
    "Flu",
    "Fever",
    "Cold"
]

CHRONIC_DISEASES = [
    "AIDS",
    "Hepatitis A",
    "Hepatitis B",
    "Hepatitis C",
    "Tuberculosis",
    "Cancer"
]


def chatbot_response(user_input, days, severity):

    disease, confidence, others = predict_disease(user_input)

    # No match
    if disease is None:
        return {
            "disease": "No disease detected",
            "confidence": 0.0,
            "precautions": ["Consult a doctor"],
            "others": [],
            "days": days,
            "severity": severity
        }

    # 🔴 FILTER EXTREME DISEASES FOR SHORT & MILD CASES
    if days <= 3 and severity <= 4 and confidence < 40:
        disease = "Viral Fever"
        confidence = min(confidence + 20, 60)
        others = ["Common Cold", "Flu"]

    precautions = PRECAUTIONS.get(disease, ["Consult a doctor"])

    return {
        "disease": disease,
        "confidence": confidence,
        "precautions": precautions,
        "others": others,
        "days": days,
        "severity": severity
    }

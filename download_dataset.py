import kagglehub

# Download latest version
path = kagglehub.dataset_download(
    "kaushil268/disease-prediction-using-machine-learning"
)

print("Path to dataset files:", path)

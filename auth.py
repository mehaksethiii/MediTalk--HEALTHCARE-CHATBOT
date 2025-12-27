import pandas as pd
import hashlib
import os

FILE = "users.csv"

def init():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        pd.DataFrame(columns=["username", "password"]).to_csv(FILE, index=False)

init()

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def signup(u, p):
    df = pd.read_csv(FILE)
    if u in df["username"].values:
        return False
    df.loc[len(df)] = [u, hash_pass(p)]
    df.to_csv(FILE, index=False)
    return True

def login(u, p):
    df = pd.read_csv(FILE)
    return ((df["username"] == u) & (df["password"] == hash_pass(p))).any()

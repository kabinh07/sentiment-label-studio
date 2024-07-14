from label_studio_sdk.client import LabelStudio
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import os
import re

load_dotenv(override=True)

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

print(BASE_URL)
print(API_KEY)

ls = LabelStudio(base_url = BASE_URL, api_key = API_KEY)

print(ls)

projects = ls.projects.list().dict()

print(projects)

# for item in projects['items']:
#     project_id = item["id"]

pattern_1 = re.compile(r"[:;<=][3PD)(poOC0\*/\\=-][3PD)(poO\*]*")
pattern_2 = re.compile(r"([.,:%$&!।?])\1+")
pattern_3 = re.compile(r"([.,:%$&!।?]\s)\1+")
pattern_4 = re.compile(r'[\u2000-\u3300]|[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]')
pattern_5 = re.compile(r"[-T^>][o_.][-T^<]")

def data_cleaning(text):
    text = pattern_1.sub(" ", text)
    text = pattern_2.sub(r"\1", text)
    text = pattern_3.sub(r"\1", text)
    text = pattern_4.sub(" ", text)
    text = pattern_5.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text

df = pd.read_csv("data/combined_data.csv")
print(df.shape)
df.dropna(inplace = True)
print(df.shape)
df["text"] = df["text"].apply(data_cleaning)
indexes = []
for idx, data in df.iterrows():
    if data["text"] == "" or data["text"] == " ":
        indexes.append(idx)
df.dropna(inplace = True)
df.drop(indexes, inplace=True)
print(df.shape)
df.reset_index(drop=True, inplace=True)
print(df.shape)
data = []
for idx, row in tqdm(df[:1000].iterrows(), total=1000):
    text = row["text"]
    data.append({"text": text})
    if (idx+1) % 100 == 0:
        ls.projects.import_tasks(
            id=1,
            request= data
        )
        data = []


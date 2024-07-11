from label_studio_sdk.client import LabelStudio
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
project_id = os.getenv("PROJECT_ID")

ls = LabelStudio(base_url = base_url, api_key = api_key)

projects = ls.projects.list().dict()

print(projects)

# for item in projects['items']:
#     project_id = item["id"]

df = pd.read_csv("data/combined_data.csv")
print(df.shape)
df.dropna(inplace = True)
print(df.shape)
indexes = []
for idx, data in df.iterrows():
    if data["text"] == "":
        indexes.append(idx)
df.drop(indexes, inplace=True)
print(df.shape)
data = []
for idx, row in tqdm(df.iterrows(), total=len(df)):
    text = row["text"]
    data.append({"text": text})
    if (idx+1) % 100 == 0:
        ls.projects.import_tasks(
            id=1,
            request= data
        )
        data = []


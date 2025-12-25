import pandas as pd

CSV_PATH = "data/full_dataset.csv"

df = pd.read_csv(CSV_PATH)
print(df.columns)

df = df.rename(columns={df.columns[0]: "id"})
df["id"] = df["id"].astype(int)
df.to_csv(CSV_PATH, index=False, encoding="utf-8")

df_check = pd.read_csv(CSV_PATH)
print(df_check.columns)
import pandas as pd
import os

RAW_FOLDER = "data/raw"

all_data = []

for file in os.listdir(RAW_FOLDER):

    if file.endswith(".xlsx"):

        path = os.path.join(RAW_FOLDER, file)

        df = pd.read_excel(path)

        all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

combined_df.columns = (
    combined_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

combined_df.drop_duplicates(inplace=True)

combined_df["opening_rank"] = (
    combined_df["opening_rank"]
    .astype(str)
    .str.replace("P", "", regex=False)
)

combined_df["closing_rank"] = (
    combined_df["closing_rank"]
    .astype(str)
    .str.replace("P", "", regex=False)
)

combined_df["opening_rank"] = pd.to_numeric(
    combined_df["opening_rank"],
    errors="coerce"
)

combined_df["closing_rank"] = pd.to_numeric(
    combined_df["closing_rank"],
    errors="coerce"
)

combined_df.dropna(
    subset=["opening_rank", "closing_rank"],
    inplace=True
)

combined_df["opening_rank"] = combined_df["opening_rank"].astype(int)
combined_df["closing_rank"] = combined_df["closing_rank"].astype(int)

combined_df.to_csv(
    "data/cleaned/josaa_cleaned.csv",
    index=False
)

print(combined_df.shape)
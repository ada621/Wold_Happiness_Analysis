import pandas as pd


def classify_happiness(score: float) -> str:
    if score >= 6.5:
        return "High"
    elif score >= 5.5:
        return "Above Average"
    elif score >= 4.5:
        return "Average"
    elif score >= 3.5:
        return "Low"
    else:
        return "Very Low"

def enrich_dataframe(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df["Happiness Score"] = pd.to_numeric(df["Happiness Score"], errors="coerce")
    df["Happiness Label"] = df["Happiness Score"].apply(classify_happiness)
    df["Year"] = year

    return df

def main():
   file_2018 = "2018.csv"
   file_2019 = "2019.csv"

   df_2018 = pd.read_csv(file_2018, encoding="utf-8")
   df_2019 = pd.read_csv(file_2019, encoding="utf-8")


   df_2018 = enrich_dataframe(df_2018, 2018)
   df_2019 = enrich_dataframe(df_2019, 2019)


   df_2018.to_csv("2018_updated.csv", index=False, encoding="utf-8")
   df_2019.to_csv("2019_updated.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()

   
import os
import glob
import pandas as pd


def load_csvs_from_folder(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    dataframes = []

    for file in csv_files:
        df = pd.read_csv(file)
        df["SourceFile"] = os.path.basename(file)
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def find_column(df, possible_names):
    for col in df.columns:
        clean_col = col.strip().lower().replace(" ", "").replace("_", "").replace("\ufeff", "")

        for name in possible_names:
            clean_name = name.strip().lower().replace(" ", "").replace("_", "").replace("\ufeff", "")

            if clean_col == clean_name:
                return col

    return None


def clean_percentage_column(series):
    return (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace("nan", None)
        .pipe(pd.to_numeric, errors="coerce")
    )


def clean_health_dataset(df, value_name):
    state_col = find_column(df, [
        "LocationDesc",
        "State",
        "Location",
        "StateName",
        "\ufeffState"
    ])

    value_col = find_column(df, [
        "Data_Value",
        "Value",
        "Percent",
        "Percentage",
        "DataValue",
        "Prevalence",
        "Yes"
    ])

    year_col = find_column(df, [
        "Year",
        "YearStart",
        "DataYear"
    ])

    if state_col is None:
        raise ValueError(f"Could not find state/location column in {value_name} dataset.")

    if value_col is None:
        raise ValueError(f"Could not find data value column in {value_name} dataset.")

    cleaned = df[[state_col, value_col]].copy()

    cleaned = cleaned.rename(columns={
        state_col: "State",
        value_col: value_name
    })

    if year_col is not None:
        cleaned["Year"] = df[year_col]
    else:
        cleaned["Year"] = 2024

    cleaned[value_name] = clean_percentage_column(cleaned[value_name])
    cleaned = cleaned.dropna(subset=["State", value_name])

    cleaned = cleaned.groupby(["State", "Year"], as_index=False)[value_name].mean()

    return cleaned


def assign_business_strategy(row):
    obesity = row["Obesity"]
    inactivity = row["Inactivity"]
    tobacco = row["Tobacco"]

    if obesity >= 35 or inactivity >= 30 or tobacco >= 25:
        return "Enhanced Risk Review"
    else:
        return "Standard Product Review"


def build_combined_dataset():
    obesity_raw = load_csvs_from_folder("./health_data/obesity")
    inactivity_raw = load_csvs_from_folder("./health_data/inactivity")
    tobacco_raw = load_csvs_from_folder("./health_data/tobacco")

    obesity = clean_health_dataset(obesity_raw, "Obesity")
    inactivity = clean_health_dataset(inactivity_raw, "Inactivity")
    tobacco = clean_health_dataset(tobacco_raw, "Tobacco")

    df = obesity.merge(inactivity, on=["State", "Year"], how="inner")
    df = df.merge(tobacco, on=["State", "Year"], how="inner")

    if df.empty:
        print("No exact State/Year matches found. Merging by State only...")

        obesity_state = obesity.groupby("State", as_index=False)["Obesity"].mean()
        inactivity_state = inactivity.groupby("State", as_index=False)["Inactivity"].mean()
        tobacco_state = tobacco.groupby("State", as_index=False)["Tobacco"].mean()

        df = obesity_state.merge(inactivity_state, on="State", how="inner")
        df = df.merge(tobacco_state, on="State", how="inner")

    df = df.dropna()

    if len(df) < 5:
        raise ValueError("Not enough merged data to train models. Check the CSV files.")

    df["BusinessStrategy"] = df.apply(assign_business_strategy, axis=1)

    return df
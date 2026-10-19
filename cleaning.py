# data cleaning

import pandas as pd

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Duplicate rows removed: {before - after}")
    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = df.shape[0]
        df = df.dropna()
        after = df.shape[0]
        print(f"Rows with missing values removed: {before - after}")
        return df

    elif axis == "columns":
        before = df.shape[1]
        df = df.dropna(axis=1)
        after = df.shape[1]
        print(f"Columns with missing values removed: {before - after}")
        return df

    else: 
        print(f"Unsupported axis: {axis}")


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    before = len(df)

    for col in columns:
        if col not in df.columns:
            print(f"Column {col} does not exist; skipping")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"Column {col} is not numeric; skipping")
            continue

        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            df = df[(df[col] <= upper) & (df[col] >= lower)]
        elif method == "zscore":
            mean = df[col].mean()
            std = df[col].std()
            z_scores = (df[col] - mean) / std
            df = df[z_scores.abs() <= threshold]

    after = len(df)

    print(f"{before - after} rows removed from {columns} via {method} with {threshold} threshold")
    
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    summ = {}

    summ["rows_before"] = len(df_before)
    summ["rows_after"] = len(df_after)
    summ["rows_removed"] = len(df_before) - len(df_after)
    summ["columns_before"] = df_before.shape[1]
    summ["columns_after"] = df_after.shape[1]
    summ["columns_removed"] = df_before.shape[1] - df_after.shape[1]

    return summ
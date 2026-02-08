
def clean_data(df):
    """
    Clean GDP dataset:
    - Remove rows with missing GDP values
    - Ensure GDP columns are numeric
    """
    df = df.copy()

    # Convert all year columns to numeric where possible
    year_cols = [col for col in df.columns if isinstance(col, int)]

    df[year_cols] = df[year_cols].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )

    # Drop rows where all GDP values are missing
    df = df.dropna(subset=year_cols, how="all")

    return df

def processGDP(df, config):

    continent =config["region"]
    filterregion=df[df["Continent"]==continent]
    print(filterregion)
    year=config["year"]
    yeardata=filterregion[year]
    print(yeardata)

    operation=config["operation"]

    if operation=="average":
        result=yeardata.mean()

    elif operation=="sum":
        result=yeardata.sum()

    else:
        result = none
        print("invalid operation")

    return result

    def reshape_data(df):
    pass

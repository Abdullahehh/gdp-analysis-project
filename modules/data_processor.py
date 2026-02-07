
def clean_data(df):
 
    df = df.copy()

   
    year_cols = [col for col in df.columns if isinstance(col, int)]

    df[year_cols] = df[year_cols].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )

    df = df.dropna(subset=year_cols, how="all") #agr hm how="any" use kren koi koi aik col b agr missing ho ga to 
    #  row remove ho jae gi

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

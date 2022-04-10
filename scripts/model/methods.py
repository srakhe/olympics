import pandas as pd

def bootstrap(df, final_rows):
    cols = df.columns.values.tolist()
    bs_data = pd.DataFrame(columns=cols)
    for i in bs_data:
        bs_data[i].fillna(bs_data[i].mean(), inplace=True)

    for i in range(final_rows):
        df_inbet = df.sample(n=5, replace=True)
        dict_vals = {}
        for i in cols:
            dict_vals[i] = df_inbet[i].mean()
        bs_data = bs_data.append(dict_vals, ignore_index=True)
    
    return bs_data
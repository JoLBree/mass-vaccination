import pandas as pd
import numpy as np

new_week = "apr_22"
prev_week = "apr_15"

def calculate_percent(row):
	return row["at_least_one"] / row["Population"] * 100

df = pd.read_csv("original.csv", thousands=",")
df["Population"] = df["Population"].str.strip()
df["Population"]= df["Population"].str.replace(',', '')
df = df[~df["Population"].str.contains("-")]
df["Population"]= df["Population"].astype(np.int64)


df["at_least_one"] = df["at_least_one"].str.strip()
df["at_least_one"]= df["at_least_one"].str.replace(',', '')
df = df[~df["at_least_one"].str.contains("-")]
df = df[~df["at_least_one"].str.contains(r'[@#&$%+-/*]')]
df["at_least_one"]= df["at_least_one"].astype(np.int64)

df = df[df["Age Group"] == "Total"]
df['percent'] = df.apply(calculate_percent, axis=1)
df = df.sort_values("percent")
df.to_csv("output.csv")

# ======

df = pd.read_csv("original.csv", thousands=",")
df["Population"] = df["Population"].str.strip()
df["Population"]= df["Population"].str.replace(',', '')
df = df[~df["Population"].str.contains("-")]
df["Population"]= df["Population"].astype(np.int64)


df["at_least_one"] = df["at_least_one"].str.strip()
df["at_least_one"]= df["at_least_one"].str.replace(',', '')
df = df[~df["at_least_one"].str.contains("-")]
df = df[~df["at_least_one"].str.contains(r'[@#&$%+-/*]')]
df["at_least_one"]= df["at_least_one"].astype(np.int64)

df = df[df["Age Group"] != "Total"]
df["Age Group"]= df["Age Group"].str.replace(' Years', '')

# set(df["Age Group"].values)
# {'0-19', '20-29', '30-49', '50-64', '65-74', '75+'}
df = df[(df["Age Group"] == "20-29") | (df["Age Group"] == "30-49")]
df = df.groupby("Town").sum()

df['percent'] = df.apply(calculate_percent, axis=1)
df = df.sort_values("percent")
df.to_csv("young.csv")

# =====

df = pd.read_csv("original.csv", thousands=",")
df["Population"] = df["Population"].str.strip()
df["Population"]= df["Population"].str.replace(',', '')
df = df[~df["Population"].str.contains("-")]
df["Population"]= df["Population"].astype(np.int64)


df["at_least_one"] = df["at_least_one"].str.strip()
df["at_least_one"]= df["at_least_one"].str.replace(',', '')
df = df[~df["at_least_one"].str.contains("-")]
df = df[~df["at_least_one"].str.contains(r'[@#&$%+-/*]')]
df["at_least_one"]= df["at_least_one"].astype(np.int64)

df = df[df["Age Group"] != "Total"]
df["Age Group"]= df["Age Group"].str.replace(' Years', '')

# set(df["Age Group"].values)
# {'0-19', '20-29', '30-49', '50-64', '65-74', '75+'}
df = df[(df["Age Group"] == "50-64") | (df["Age Group"] == "65-74") | (df["Age Group"] == "75+")]
df = df.groupby("Town").sum()

df['percent'] = df.apply(calculate_percent, axis=1)
df = df.sort_values("percent")
df.to_csv("old.csv")



young = pd.read_csv("young.csv")
old = pd.read_csv("old.csv")
df = young.merge(old, on="Town", suffixes=["_young", "_old"])
df["percent_difference"] = df.apply(lambda row: row["percent_old"] - row["percent_young"], axis=1)
df = df.sort_values("percent_difference")
df.to_csv("young_and_old.csv", index=False)

# =======



df = pd.read_csv(f"young_and_old.csv")

df = df.merge(pd.read_csv(f"{prev_week}/young_and_old_{prev_week}.csv"), on="Town", suffixes=["_new", "_previous"])

df[f"absolute_growth_{new_week}"] = df.apply(lambda row: row["at_least_one_young_new"] + row["at_least_one_old_new"] -  row["at_least_one_young_previous"] - row["at_least_one_old_previous"], axis=1)
df[f"percent_growth_{new_week}"] = df.apply(lambda row: row["percent_young_new"] + row["percent_old_new"] -  row["percent_young_previous"] - row["percent_old_previous"], axis=1)

df = df[['Town', 'Population_young_new', 'at_least_one_young_new',
       'percent_young_new', 'Population_old_new', 'at_least_one_old_new',
       'percent_old_new', 'percent_difference_new', f'absolute_growth_{new_week}', f'percent_growth_{new_week}']]
df = df.rename(columns={'Population_young_new': 'Population_young',
	'at_least_one_young_new': 'at_least_one_young',
       'percent_young_new': 'percent_young',
       'Population_old_new': 'Population_old',
       'at_least_one_old_new': 'at_least_one_old',
       'percent_old_new': 'percent_old',
       'percent_difference_new': 'percent_difference',
       })

df = df.sort_values(f"percent_growth_{new_week}")

df.to_csv(f"growth.csv", index=False)


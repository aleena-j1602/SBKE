import pandas as pd
df=pd.read_csv("https://raw.githubusercontent.com/jgalazka/SB_publications/refs/heads/main/SB_publication_PMC.csv")
links=df.iloc[:, 1]
linklist=links.tolist()
print(linklist)
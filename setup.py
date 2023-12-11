import pandas as pd
from K_means import Kmeans

centroides_str = None

with open("centroides.txt", 'r') as f:
    centroides_str = f.readline()

centroides_str = centroides_str[1:-1].split('], ')

centroides = []

for c in centroides_str:
    cent = c[1:].split(', ')
    f_cent = []
    for k in cent:
        try:
            f_cent.append(float(k))

        except:
            f_cent.append(float(k[:-1]))
    
    centroides.append(f_cent)

full_df = pd.read_csv('genres_v2.csv', low_memory=False)
columns = full_df.columns

ind = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
dep = [c for c in columns if c not in ind]
df = full_df[ind]

print("Iniciando el sistema...")

km = Kmeans(df, len(centroides))
km.centroides = centroides
assert(km.centroides == centroides)
km.train(1)
final_df = km.X.join(full_df[dep])
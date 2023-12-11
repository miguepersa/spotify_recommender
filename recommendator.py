from setup import km, final_df, ind
from spotify_login import spotify
from random import randint

def recommendation(song_info, n_songs = 1):
    cluster = km.get_cluster(song_info)
    df = final_df[final_df['cluster'] == cluster]
    
    songs = [(song['song_name'], song['id']) for _,song in df.iterrows()]
    
    recommendations = []
    while len(recommendations) != n_songs:
        s = songs[randint(0,len(songs)-1)]

        if isinstance(s[0], float) or s in recommendations:
            continue
        
        recommendations.append(s)

    print("Aqui tiene una lista de canciones que pueden gustarle:")
    for song in recommendations:
        print(f"- {song[0]} (https://open.spotify.com/intl-es/track/{song[1]})")

def get_song_data(id):
    data = spotify.audio_features(id)
    song_data = [data[0][k] for k in ind]
    return song_data

def get_song_id(link):
    parts = link.split('/')
    song_id = parts[-1].split('?')[0]
    return song_id

if __name__ == '__main__':
    print("Bienvenido a Spotify-reccomendator.\n")
    while True:
        link = input("Ingrese el enlace de su cancion favorita \n(el enlace se obtiene presionando \"Compartir -> Copiar enlace de la cancion\" en Spotify): ")

        if link.lower() == "salir":
            break

        song_id = get_song_id(link)
        info = get_song_data(song_id)
        n = int(input("Ingrese el numero de recomendaciones deseado: "))
        recommendation(info, n)
        print()
        print()
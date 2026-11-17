from museum.artists import get_artists

def main():
    artists = input("Artist: ")
    artists = get_artists(query=artists, limit=3)
    for artist in artists:
        print(f"* {artist}")


main()
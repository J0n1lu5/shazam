import uuid
from tinydb import TinyDB, Query
from serializer import serializer
from collections import defaultdict

class AudioDatabase:
    def __init__(self, db_path):
        self.db = TinyDB(db_path, storage=serializer)

    def setup_db(self):
        # Create tables if they don't exist
        self.db.table('hash')
        self.db.table('song_info')
        self.db.table('search_history')

    def song_in_db(self, hashes):
        Song = Query()
        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, hashes[0][2]).int)  
        return bool(self.db.table('song_info').search(Song.song_id == song_id))


    def store_song(self, hashes, song_info):
        if len(hashes) < 1:
            return

        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, song_info[1]).int)  
        hash_entries = [{'hash': h[0], 'offset': h[1], 'song_id': song_id} for h in hashes]
        self.db.table('hash').insert_multiple(hash_entries)

        song_info_entry = {'title': song_info[0] or "Unknown",                           
                           'artist': song_info[1] or "Unknown",
                           'song_id': song_id}
        self.db.table('song_info').insert(song_info_entry)

    def get_matches(self, hashes, threshold=5):
        hash_values = [h[0] for h in hashes]
        results = self.db.table('hash').search(Query().hash.one_of(hash_values))

        # Erstellen Sie ein Dictionary, um die Ergebnisse zu speichern
        result_dict = defaultdict(list)
        for r in results:
            # Verwenden Sie den hash-Wert als Schlüssel für das Dictionary
            result_dict[r['hash']].append((r['offset'], r['song_id']))

        matches = {}
        for hash_value, song_offsets in result_dict.items():
            # Iterieren Sie über die Song-Offsets und zählen Sie die Anzahl der Übereinstimmungen
            song_id_count = defaultdict(int)
            for offset, song_id in song_offsets:
                song_id_count[song_id] += 1

            # Überprüfen Sie, ob die Anzahl der Übereinstimmungen über dem Schwellenwert liegt
            for song_id, count in song_id_count.items():
                if count >= threshold:
                    song_info = self.get_info_for_song_id(song_id)
                    if song_info is not None:
                        artist = song_info['artist']
                        title = song_info['title']
                        matches[song_id] = (artist, title, count)

        return matches

        

    def get_info_for_song_id(self, song_id):
        Song = Query()
        song_info = self.db.table('song_info').get(Song.song_id == song_id)

        if song_info is None:
            return None
        
        return song_info 
    

    def store_history(self,song_info):
        
        #song_info = {'title': song_info[0],'artist': song_info[1]}
        self.db.table('search_history').insert(song_info)

    def get_history(self,limit):
        # Abrufen der letzten erkannten Songs nach Einfügezeitpunktsortiert
        recent_songs = self.db.table('search_history').all()
        recent_songs.sort(key=lambda x: x.doc_id, reverse=True)  # Sortieren nach Einfügezeitpunkt (doc_id)

        # Begrenzen der Anzahl der zurückgegebenen Songs auf 'limit'
        
        recent_songs = recent_songs[:limit]

        # Rückgabe der Liste der zuletzt erkannten Songs
        return recent_songs
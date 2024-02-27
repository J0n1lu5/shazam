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

    def song_in_db(self, hashes):
        Song = Query()
        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, hashes[0][2]).int)  
        return bool(self.db.table('song_info').search(Song.song_id == song_id))


    def store_song(self, hashes, song_info):
        if len(hashes) < 1:
            return

        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, song_info[2]).int)  
        hash_entries = [{'hash': h[0], 'offset': h[1], 'song_id': song_id} for h in hashes]
        self.db.table('hash').insert_multiple(hash_entries)

        song_info_entry = {'artist': song_info[0] or "Unknown",
                           'album': song_info[1] or "Unknown",
                           'title': song_info[2] or "Unknown",
                           'song_id': song_id}
        self.db.table('song_info').insert(song_info_entry)

    def get_matches(self, hashes, threshold=5):
        hash_values = [h[0] for h in hashes]
        results = self.db.table('hash').search(Query().hash.one_of(hash_values))

        h_dict = {h[0]: h[1] for h in hashes}
        result_dict = defaultdict(list)
        for r in results:
            result_dict[r['song_id']].append((r['offset'], h_dict[r['hash']]))

        matches = []
        for song_id, offsets in result_dict.items():
            artist, album, title = self.get_info_for_song_id(song_id)
            matches.append((song_id, artist, album, title, len(offsets)))

        return matches

    def get_info_for_song_id(self, song_id):
        Song = Query()
        song_info = self.db.table('song_info').get(Song.song_id == song_id)
        return song_info['artist'], song_info['album'], song_info['title']

import os
import logging
from multiprocessing import Pool, Lock, current_process
import numpy as np
from tinytag import TinyTag
import settings
#from .record import record_audio
from Fingerprint import AudioFingerprinter
from database_storage import AudioDatabase
#from .storage import store_song, get_matches, get_info_for_song_id, song_in_db, checkpoint_db

KNOWN_EXTENSIONS = ["mp3", "wav", "flac", "m4a"]


class SongRecognizer:
    def __init__(self, db_path):
        self.db = AudioDatabase(db_path)
        self.lock = Lock()
        self.db.setup_db()

    def get_song_info(self, filename):
        """Gets the ID3 tags for a file. Returns None for tuple values that don't exist."""
        tag = TinyTag.get(filename)
        artist = tag.artist if tag.albumartist is None else tag.albumartist
        return (artist, tag.album, tag.title)

    def register_song(self, filename):
        """Register a single song."""
        if self.db.song_in_db(filename):
            return
        hashes = self.fingerprint_file(filename)
        song_info = self.get_song_info(filename)
        try:
            logging.info(f"{current_process().name} waiting to write {filename}")
            with lock:
                logging.info(f"{current_process().name} writing {filename}")
                self.db.store_song(hashes, song_info)
                logging.info(f"{current_process().name} wrote {filename}")
        except NameError:
            logging.info(f"Single-threaded write of {filename}")
            # running single-threaded, no lock needed
            self.db.store_song(hashes, song_info)

    def register_directory(self, path):
        """Recursively register songs in a directory."""
        def pool_init(l):
            """Init function that makes a lock available to each of the workers in
            the pool. Allows synchronisation of db writes since SQLite only supports
            one writer at a time."""
            global lock
            lock = l
            logging.info(f"Pool init in {current_process().name}")

        to_register = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.split('.')[-1] not in KNOWN_EXTENSIONS:
                    continue
                file_path = os.path.join(path, root, f)
                to_register.append(file_path)
        l = Lock()
        with Pool(settings.NUM_WORKERS, initializer=pool_init, initargs=(l,)) as p:
            p.map(self.register_song, to_register)
        # speed up future reads
        self.db.checkpoint_db()

    def score_match(self, offsets):
        """Score a matched song."""
        binwidth = 0.5
        tks = list(map(lambda x: x[0] - x[1], offsets))
        hist, _ = np.histogram(tks,
                               bins=np.arange(int(min(tks)),
                                              int(max(tks)) + binwidth + 1,
                                              binwidth))
        return np.max(hist)
    """
    def best_match(self, matches):
        if not matches:
            return None

        # Find the song with the most offsets
        best_match = max(matches, key=lambda k: matches[k][3])

        return best_match, matches[best_match]
    """
    
    def best_match(self, matches):
        #For a dictionary of song_id: offsets, returns the best song_id.
        matched_song = None
        best_score = 0
        for song_id, offsets in matches.items():
            if len(offsets) < best_score:
                continue
            score = self.score_match(offsets)
            if score > best_score:
                best_score = score
                matched_song = song_id
        return matched_song
    

    def recognise_song(self, filename):
        """Recognises a pre-recorded sample."""
        hashes = self.fingerprint_file(filename)
        matches = self.db.get_matches(hashes)
        matched_song = self.best_match(matches)
        if matched_song is None:
            return None
        info = self.db.get_info_for_song_id(matched_song)
        if info is not None:
            return info
        return matched_song

    """def listen_to_song(self, filename=None):
        Recognises a song using the microphone.
        audio = record_audio(filename=filename)
        hashes = self.fingerprint_audio(audio)
        matches = get_matches(hashes)
        matched_song = self.best_match(matches)
        info = get_info_for_song_id(matched_song)
        if info is not None:
            return info
        return matched_song"""

    def fingerprint_file(self, filename):
        """Generate hashes for a file."""
        fingerprinter = AudioFingerprinter()
        return fingerprinter.fingerprint_file(filename)

    def fingerprint_audio(self, frames):
        """Generate hashes for a series of audio frames."""
        fingerprinter = AudioFingerprinter()
        return fingerprinter.fingerprint_audio(frames)


import os
from tinydb import TinyDB, Query
from serializer import serializer


class Data ():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('Songs')

    def __init__ (self, song_name : str, interpret : str):
        self.song_name = song_name
        self.interpret = interpret
        self.is_active = True

    def __str__(self):
            return f'Device {self.song_name} ({self.interpret})'

    def __repr__(self):
            return self.__str__()

    def store_data(self):
            print("Storing data...")
            # Check if the song already exists in the database
            SongQuery = Query()
            result = self.db_connector.search(SongQuery.song_name == self.song_name)
            if result:
                # Update the existing record with the current instance's data
                result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
                print("Data updated.")
            else:

                
                # If the song doesn't exist, insert a new record
                self.db_connector.insert(self.__dict__)
                print("Data inserted.")



    def delete_data(self):
        print("Deleting data...")
        SongQuery = Query()
        result = self.db_connector.remove(SongQuery.song_name == self.song_name)
        print(f"Deleted {result}")



    @classmethod
    def load_data_by_device_name(cls, song_name):
        # Load data from the database and create an instance of the Song class
        SongQuery = Query()
        result = cls.db_connector.search(SongQuery.song_name == song_name)

        if result:
            data = result[0]
            return cls(data['song_name'], data['interpret'])
        
        else:
            return None
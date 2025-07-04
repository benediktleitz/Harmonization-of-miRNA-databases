from models.mirna_type import MirnaType

class MirnaEntry:
    def __init__(self, name, species, sequence, source_db, mirna_type: MirnaType, database_id=None):
        self.database_id = database_id
        self.name = name
        self.species = species
        self.sequence = sequence
        self.source_db = source_db
        self.mirna_type = mirna_type
    
    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "sequence": self.sequence,
            "source_db": self.source_db,
            "type": self.mirna_type,
            "id": self.database_id
        }
import os
from Bio import SeqIO
from models.mirna_entry import MirnaEntry
from models.mirna_type import MirnaType

class MirBaseLoader:
    def __init__(self, directory):
        self.directory = directory
        self.entries = []
        
    def load(self):

    def load_hairpin(self):
        for record in SeqIO.parse(os.path.join(self.directory, "hairpin.fa"), "fasta"):
            parts = record.description.split()
            name = parts[4] if len(parts) > 4 else "UNKOWN"
            species = parts[0].split("-")[0]
            database_id = parts[1]
            entry = MirnaEntry(name=name, species=species, sequence=record.seq, source_db="miRBase", 
                               mirna_type=MirnaType.pre, database_id=database_id)
            self.entries.append(entry)
            if len(parts) <= 4:
                print(f" Warning: Unexpected header format: {record.description}")
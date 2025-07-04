import os
from Bio import SeqIO
from models.mirna_type import MirnaType

class MirBaseLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "miRBase.csv")
        self.source_db = "mirBase/v22.1"
        
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species,sequence,source_db,mirna_type,database_id\n")
        
        self.load_file("hairpin.fa")
        self.load_file("mature.fa")

# Create a csv file from the miRBase file that is given as input.
# The csv file will contain the following columns:
# name,species,sequence,source_db,mirna_type,database_id
    def load_file(self, filename):
        for record in SeqIO.parse(os.path.join(self.input_directory, filename), "fasta"):
            parts = record.description.split()
            name = parts[4] if len(parts) > 4 else "UNKOWN"
            species = parts[0].split("-")[0].lower()
            database_id = parts[1]
            with open(self.output_file, "a") as output_file:
                output_file.write(f"{name},{species},{record.seq.upper()},{self.source_db},{MirnaType.pre.value},{database_id}\n")
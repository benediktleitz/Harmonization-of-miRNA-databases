import os
from Bio import SeqIO
from models.mirna_type import MirnaType

class MirBaseLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "miRBase.csv")
        self.source_db = "mirBase"
        self.source_db_version = "22.1"
        
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id\n")
        
        self.load_file("hairpin.fa", MirnaType.hairpin.value)
        self.load_file("mature.fa")

# Create a csv file from the miRBase file that is given as input.
# The csv file will contain the following columns:
# name,taxon_id,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id
    def load_file(self, filename, mirna_type=MirnaType.mature.value):
        for record in SeqIO.parse(os.path.join(self.input_directory, filename), "fasta"):
            parts = record.description.split()
            name = parts[0].split("-", 1)[1]

            # Change name starts MIR and mir to miR
            if name.startswith("MIR") or name.startswith("mir"):
                name = "miR" + name[3:]
            
            # Extract species name and abbreviation, depending of type of miRNA the species name is at different positions
            if mirna_type == MirnaType.hairpin.value:
                species_name = " ".join(parts[2:-2])
            else:
                species_name = " ".join(parts[2:-1])
            
            species_abbr = parts[0].split("-")[0].lower()
            database_id = parts[1]
            with open(self.output_file, "a") as output_file:
                output_file.write(f"{name},{species_name},{species_abbr},{record.seq.upper()},{self.source_db},{self.source_db_version},{mirna_type},{database_id}\n")
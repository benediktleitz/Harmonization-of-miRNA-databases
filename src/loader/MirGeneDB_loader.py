import os
from Bio import SeqIO
from models.mirna_type import MirnaType

class MirGeneDBLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "MirGeneDB.csv")
        self.source_db = "mirGeneDB"
        self.source_db_version = "v3.0"
        
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id\n")
        
        self.load_file("all_sequences")

    def load_file(self, filename):
        for record in SeqIO.parse(os.path.join(self.input_directory, filename), "fasta"):
            species_abbr, interim_name = record.description.split("-", maxsplit=1)
            species_abbr = species_abbr.lower()

            if interim_name[-3:] == "pre":
                mirna_type = MirnaType.pre.value
            elif interim_name[-3:] == "pri":
                mirna_type = MirnaType.pri.value
            elif interim_name[-4:] == "loop":
                mirna_type = MirnaType.loop.value
            else:
                mirna_type = MirnaType.mature.value # The * ist lost here

            if mirna_type == MirnaType.mature.value:
                name = interim_name.replace("_", "-").replace("*", "")
            else:
                name = interim_name.split("_")[0]
            # Change the name to be consistent with miRBase
            name = name[0].lower() + name[1:]
            name = name.replace("mir", "miR")
            with open(self.output_file, "a") as output_file:
                output_file.write(f"{name},species_name,{species_abbr},{record.seq.upper()},{self.source_db},{self.source_db_version},{mirna_type},NA\n")
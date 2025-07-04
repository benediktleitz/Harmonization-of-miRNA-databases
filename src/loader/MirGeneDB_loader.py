import os
from Bio import SeqIO
from models.mirna_type import MirnaType

class MirGeneDBLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "mirGeneDB.csv")
        self.mirbase_version = "mirGeneDB"
        
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species,sequence,source_db,mirna_type,database_id\n")
        
        self.load_file("all_sequences")

    def load_file(self, filename):
        for record in SeqIO.parse(os.path.join(self.input_directory, filename), "fasta"):
            parts = record.description.split("-", maxsplit=1)
            species = parts[0].lower()

            interim_name = parts[1]
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

            with open(self.output_file, "a") as output_file:
                output_file.write(f"{name},{species},{record.seq.upper()},{self.mirbase_version},{mirna_type},NA\n") # Should I give AC here?
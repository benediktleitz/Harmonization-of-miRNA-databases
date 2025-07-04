import os
import csv
from models.mirna_type import MirnaType

class VIRmiRNALoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "VIRmiRNA.csv")
        self.source_db = "VIRmiRNA"
        self.seen_pre_miRNAs = set()
    
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species,sequence,source_db,mirna_type,database_id\n")
        self.load_file(os.path.join(self.input_directory, "vmr.tsv"))

# Create a csv file from the PmiREN file that is given as input.
# The csv file will contain the following columns:
# name,species,sequence,source_db,mirna_type,database_id
# It could easily be extended to include more information if needed, like the genomic coordinates.
    def load_file(self, file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file, delimiter="\t")
            for row in reader:
                name = "-".join(row["miRNA"].split("-")[1:]) # Extract the miRNA name without the species prefix
                species = row["Virus"].lower()
                sequence = row["miRNA_Sequence"]
                name_pre = "-".join(row["Pre_miRNA"].split("-")[1:]) # Extract the miRNA name without the species prefix
                database_id = row["ID"]
                with open(self.output_file, "a") as output_file:
                    if name_pre not in self.seen_pre_miRNAs:
                        sequence_pre = row["Pre_miRNA_Sequence"]
                        output_file.write(f"{name_pre},{species},{sequence_pre},{self.source_db},{MirnaType.pre.value},{database_id}\n")
                        self.seen_pre_miRNAs.add(name_pre)
                    output_file.write(f"{name},{species},{sequence},{self.source_db},{MirnaType.mature.value},{database_id}\n")

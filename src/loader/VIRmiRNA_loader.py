import os
import csv
from models.mirna_type import MirnaType

class VIRmiRNALoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "VIRmiRNA.csv")
        self.source_db = "VIRmiRNA"
        self.source_db_version = "NA"
        self.seen_pre_miRNAs = set()
    
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id\n")
        self.load_file(os.path.join(self.input_directory, "vmr.tsv"))

# Create a csv file from the PmiREN file that is given as input.
# The csv file will contain the following columns:
# name,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id
# It could easily be extended to include more information if needed, like the genomic coordinates.
    def load_file(self, file_path):
        with open(file_path, "r") as file, open(self.output_file, "a") as output_file:
            reader = csv.DictReader(file, delimiter="\t")
            for row in reader:
                name = "-".join(row["miRNA"].split("-")[1:]) # Extract the miRNA name without the species prefix
                species_name = row["Virus full name"]
                species_abbr = row["Virus"].lower()
                sequence = row["miRNA_Sequence"].upper()
                name_pre = row["Pre_miRNA"]
                if name_pre == "na":
                    name_pre = "na"
                else:
                    if name_pre.startswith("pre-"):
                        name_pre = "-".join(name_pre.split("-")[1:])
                    name_pre = "-".join(name_pre.split("-")[1:])

                database_id = row["ID"]
                
                if name_pre not in self.seen_pre_miRNAs and name_pre != "na":
                    sequence_pre = row["Pre_miRNA_Sequence"].upper()
                    output_file.write(f"{name_pre},{species_name},{species_abbr},{sequence_pre},{self.source_db},{self.source_db_version},{MirnaType.pre.value},{database_id}\n")
                    self.seen_pre_miRNAs.add(name_pre)
                output_file.write(f"{name},{species_name},{species_abbr},{sequence},{self.source_db},{self.source_db_version},{MirnaType.mature.value},{database_id}\n")

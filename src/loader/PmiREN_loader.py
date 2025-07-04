import os
import csv
from models.mirna_type import MirnaType

class PmiRENLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "PmiREN.csv")
        self.source_db = "PmiREN"
    
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species,sequence,source_db,mirna_type,database_id\n")
        for root, dirs, files in os.walk(self.input_directory):
            for file in files:
                if file.endswith("basicInfo.txt"):
                    file_path = os.path.join(root, file)
                    self.load_file(file_path)

# Create a csv file from the PmiREN file that is given as input.
# The csv file will contain the following columns:
# name,species,sequence,source_db,mirna_type,database_id
# It could easily be extended to include more information if needed, like the genomic coordinates.
    def load_file(self, file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file, delimiter="\t")
            for row in reader:
                name_pre = row["miRNA_locus_ID"].split("-")[1]
                species = row["miRNA_locus_ID"].split("-")[0].lower()
                database_id = row["miRNA_locus_accession"]
                sequence_pre = row["Stem_loop_seq"]
                mature_seq = row["mature_seq"]
                star_seq = row["star_seq"]

                # Convert star/non start to 5p/3p based on strand and start positions
                strand = row["Strand"]
                mature_start = int(row["mature_start"])
                star_start = int(row["star_start"])
                if strand == "+":
                    mature_is_5p = mature_start < star_start
                else:
                    mature_is_5p = mature_start > star_start
                
                name_mature = f"{name_pre}-5p" if mature_is_5p else f"{name_pre}-3p"
                name_star = f"{name_pre}-3p" if mature_is_5p else f"{name_pre}-5p"
                
                with open(self.output_file, "a") as output_file:
                    output_file.write(f"{name_pre},{species},{sequence_pre}, {self.source_db},{MirnaType.pre.value},{database_id}\n")
                    output_file.write(f"{name_mature},{species},{mature_seq}, {self.source_db},{MirnaType.mature.value},{database_id}\n")
                    output_file.write(f"{name_star},{species},{star_seq}, {self.source_db},{MirnaType.mature.value},{database_id}\n")
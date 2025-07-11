import os
import csv
from models.mirna_type import MirnaType

class sRNAannoLoader:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_file = os.path.join(output_directory, "sRNAanno.csv")
        self.source_db = "sRNAanno"
        self.source_db_version = "NA"
        
    def load(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        with open(self.output_file, "w") as output_file:
            output_file.write("name,species_name,species_abbr,sequence,source_db,source_db_version,mirna_type,database_id\n")
        for root, dirs, files in os.walk(self.input_directory):
            for file in files:
                file_path = os.path.join(root, file)
                species_name = file.split(".", 1)[0].replace("_", " ")
                self.load_file(file_path, species_name)
    
    def load_file(self, file_path, species_name):
        with open(file_path, "r") as file, open(self.output_file, "a") as output_file:
            for line in file:
                if line.startswith("#"):
                    continue
                fields = line.strip().split("\t")
                name = fields[1]
                sequence = fields[8].split("seq=")[1]
                mirna_type = None
                if fields[2] == "miRNA_primary_transcript":
                    mirna_type = MirnaType.pri.value
                elif fields[2] == "miRNA":
                    mirna_type = MirnaType.mature.value
                
                if mirna_type is not None:
                    output_file.write(f"{name},{species_name},NA,{sequence},{self.source_db},{self.source_db_version},{mirna_type},NA\n")




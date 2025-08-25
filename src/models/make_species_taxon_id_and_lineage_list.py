#!/usr/bin/biopython
from Bio import Entrez
import pandas as pd
import time

Entrez.email = "benedikt.leitz@tum.de"
mirna_sequence_records_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv"
output_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/species_taxon_id_and_lineage.csv"
data_df = pd.read_csv(mirna_sequence_records_path, dtype={"source_db_version": str})

def query_taxon_id(species_name):
    handle = Entrez.esearch(db="taxonomy", term=species_name)
    record = Entrez.read(handle)
    if not record["IdList"]:
        return "NaN"
    time.sleep(0.34)
    return record["IdList"][0]

def query_lineage(taxon_id):
    handle = Entrez.efetch(db="taxonomy", id=taxon_id)
    record = Entrez.read(handle)
    time.sleep(0.34)
    return record[0]["Lineage"]

species_names = data_df["species_name"].unique()
i = 1
n = len(species_names)
with open(output_path, "w") as output_file:
    output_file.write("species_name,taxon_id,lineage\n")
    for species_name in species_names:
        taxon_id = query_taxon_id(species_name)
        lineage = query_lineage(taxon_id) if taxon_id != "NaN" else "NaN"
        output_file.write(f"{species_name},{taxon_id},{lineage}\n")
        print(f"Processed {i}/{n}: {species_name} -> {taxon_id}")
        i += 1

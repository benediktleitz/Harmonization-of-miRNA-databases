import pandas as pd

mirna_sequence_records_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv"
species_name_conversion_list_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/species_which_misclassified.csv"

data_df = pd.read_csv(mirna_sequence_records_path, dtype={"source_db_version": str})
conversion_df = pd.read_csv(species_name_conversion_list_path)

conversion_dict = dict(zip(conversion_df.iloc[:,0], conversion_df.iloc[:,1]))

data_df["species_name"] = data_df["species_name"].map(lambda species_name: conversion_dict.get(species_name, species_name))

data_df.to_csv(mirna_sequence_records_path, index=False)
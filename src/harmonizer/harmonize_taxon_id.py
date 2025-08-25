import pandas as pd

mirna_sequence_records_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv"
species_name_conversion_list_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/species_which_misclassified.csv"
species_map_output_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/taxon_id_species_name_and_abbr.csv"
taxon_id_map_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/species_taxon_id_and_lineage.csv"


def change_species_name(data_df, conversion_df, mirna_sequence_records_path):
    conversion_dict = dict(zip(conversion_df.iloc[:,0], conversion_df.iloc[:,1]))
    data_df["species_name"] = data_df["species_name"].map(lambda species_name: conversion_dict.get(species_name, species_name))
    data_df.to_csv(mirna_sequence_records_path, index=False)
    return data_df

def make_taxon_id_species_name_and_abbr_list(data_df, taxon_df, species_map_output_path):
    species_map = data_df[["species_name", "species_abbr"]].drop_duplicates()
    taxon_id_map = dict(zip(taxon_df["species_name"], taxon_df["taxon_id"]))

    species_map["taxon_id"] = species_map["species_name"].map(lambda name: taxon_id_map.get(name, "NaN"))

    species_map = species_map[["taxon_id", "species_name", "species_abbr"]].drop_duplicates()
    species_map.to_csv(species_map_output_path, index=False)
    return species_map

def replace_species_names_with_taxon_ids(data_df, species_map, mirna_sequence_records_path):
    combo_to_taxon_id = {
        (row["species_name"], row["species_abbr"]): row["taxon_id"]
        for _, row in species_map.iterrows()
    }

    data_df["taxon_id"] = data_df.apply(
        lambda row: combo_to_taxon_id.get((row["species_name"], row["species_abbr"]), "NaN"), axis=1
    )
    data_df = data_df.drop(columns=["species_name", "species_abbr"])
    data_df.to_csv(mirna_sequence_records_path, index=False)
    return data_df

def main():
    data_df = pd.read_csv(mirna_sequence_records_path, dtype={"source_db_version": str})
    conversion_df = pd.read_csv(species_name_conversion_list_path)
    taxon_df = pd.read_csv(taxon_id_map_path, dtype={"taxon_id": str})

    data_df = change_species_name(data_df, conversion_df, mirna_sequence_records_path)
    species_map = make_taxon_id_species_name_and_abbr_list(data_df, taxon_df, species_map_output_path)
    data_df = replace_species_names_with_taxon_ids(data_df, species_map, mirna_sequence_records_path)

if __name__ == "__main__":
    main()
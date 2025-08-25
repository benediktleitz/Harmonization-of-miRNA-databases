import pandas as pd

csv_files = ["/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/miRBase/v22.1/miRBase.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/MirGeneDB/v3.0/MirGeneDB.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/PmiREN/PmiREN.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/sRNAanno/sRNAanno.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/VIRmiRNA/VIRmiRNA.csv"]

def harmonize_miRNA_data(df_mature):

    sequence_to_id = {}
    nex_id = 1
    miRNA_records = []

    for index, row in df_mature.iterrows():
        sequence = row["sequence"]

        if sequence not in sequence_to_id:
            sequence_to_id[sequence] = nex_id
            nex_id += 1
        
        miRNA_id = sequence_to_id[sequence]
        miRNA_records.append({
                "miRNA_id": miRNA_id,
                "name": row["name"],
                "species_name": row["species_name"],
                "species_abbr": row["species_abbr"],
                "source_db": row["source_db"],
                "source_db_version": row["source_db_version"],
                "database_id": row["database_id"]
            })
    
    df_sequences = pd.DataFrame(
        [(miRNA_id, sequence) for sequence, miRNA_id in sequence_to_id.items()], columns=["miRNA_id", "sequence"]
    )
    df_records = pd.DataFrame(miRNA_records)
    return df_sequences, df_records

def main():
    dfs = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(dfs, ignore_index=True)
    df_mature = df[df["mirna_type"] == "mature"]

    df_sequences, df_records = harmonize_miRNA_data(df_mature)
    df_sequences.to_csv("/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mature_miRNA_sequence.csv", index=False)
    df_records.to_csv("/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv", index=False)

if __name__ == "__main__":
    main()

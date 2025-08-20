import pandas as pd

csv_files = ["/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/miRBase/v22.1/miRBase.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/MirGeneDB/v3.0/MirGeneDB.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/PmiREN/PmiREN.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/sRNAanno/sRNAanno.csv",
             "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/VIRmiRNA/VIRmiRNA.csv"]

dfs = [pd.read_csv(file) for file in csv_files]
df = pd.concat(dfs, ignore_index=True)
df_mature = df[df["mirna_type"] == "mature"]

sequence_to_id = {}
nex_id = 1
miRNA_data = []
miRNA_data.append("miRNA_id,name,species_name,species_abbr,source_db,source_db_version,database_id")

for index, row in df_mature.iterrows():
    sequence = row["sequence"]

    if sequence not in sequence_to_id:
        sequence_to_id[sequence] = nex_id
        nex_id += 1
    
    miRNA_id = sequence_to_id[sequence]
    miRNA_data.append(f"{miRNA_id},{row['name']},{row['species_name']},{row['species_abbr']},{row['source_db']},{row['source_db_version']},{row['database_id']}")

with open("/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mature_miRNA_sequence.csv", "w") as output_file:
    output_file.write("miRNA_id, sequence\n")
    for sequence, miRNA_id in sequence_to_id.items():
        output_file.write(f"{miRNA_id},{sequence}\n")
with open("/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv", "w") as output_file:
    output_file.write("\n".join(miRNA_data))

import pandas as pd
from Bio import SeqIO
import json

arabidopsis_fa_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/raw_data/Arabidopsis/Athaliana_447_Araport11.protein.fa"
athan_short_sequence_fa_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/raw_data/Arabidopsis/Athaliana_447_Araport11_short.protein.fa"
mmseqs_input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/mmseqs_list/seq_id_less_than_0.5_athan.list"
entity_df_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/tair_arath_df.csv"
json_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/athan_short_protein_complexes.json"
homodimer_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/uniprot_homodimer_protein_complexes.json"
# Testing dataset for the first round prediction
json_900_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/athan_900_short_protein_complexes.json"
"/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/athan_900_short_protein_complexes.json"
athan_uniprot_df_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/uniprot_arath_df.csv"


def read_lst(path):
    with open(path, "r") as file:
        lst = file.read().splitlines()
    return lst

# records = []
# # count = 0
# for record in SeqIO.parse(arabidopsis_fa_path, "fasta"):
#     # if count <= 50:
#     # Split description into fields
#     fields = record.description.split()

#     # First token is the protein ID
#     protein_id = fields[0]

#     # Parse key=value pairs
#     info = {}
#     for field in fields[1:]:
#         if "=" in field:
#             key, value = field.split("=", 1)
#             info[key] = value

#     row = {
#         "protein_id": record.id,
#         # "description": record.description,
#         "sequence": str(record.seq)[:-1],
#         "length": len(record.seq),
#         **info
#     }
    
#     records.append(row)
#         # count+=1

# df = pd.DataFrame(records)
# # df.to_csv(entity_df_output_path, index=False)

# with open(athan_short_sequence_fa_path, "w") as out:
#     count=0
#     for record in SeqIO.parse(arabidopsis_fa_path, "fasta"):
#         if len(record.seq) <= 500:
#             SeqIO.write(record, out, "fasta")
#             count+=1
# print(count)


# # print(df["protein_id"])
# # print(df.head())
# # print(df.shape)

entity_df = pd.read_csv(entity_df_output_path)
### Convert this file to csv or change name to tsv
athan_uniprot_df = pd.read_csv(athan_uniprot_df_path, sep="\t")
athan_uniprot_df["TAIR"] = athan_uniprot_df["TAIR"].str[:-1]
athan_uniprot_df = athan_uniprot_df[athan_uniprot_df['Subunit structure'].notna()]

# filter out proteins in uniprot that are also in tair
loci_list = list(set(entity_df["locus"].tolist()))
# There is no duplicated tair id in this dataset
# uniprot_tair_df = athan_uniprot_df[(athan_uniprot_df["TAIR"].isin(loci_list))&(athan_uniprot_df["Reviewed"]=="reviewed")]
uniprot_tair_df = athan_uniprot_df[(athan_uniprot_df["Reviewed"]=="reviewed")]
homodimer_uniprot_tair_df = uniprot_tair_df[uniprot_tair_df["Subunit structure"].str.contains("homodimer|Homodimer")]
homodimer_uniprot_tair_df = homodimer_uniprot_tair_df.rename(columns={'TAIR':'locus', 'Sequence': 'sequence'})
# print(len(homodimer_uniprot_tair_df))
# print(len(homodimer_uniprot_tair_df[homodimer_uniprot_tair_df.duplicated(subset=['locus'],keep=False)]))

homodimer_uniprot_tair_df = homodimer_uniprot_tair_df.merge(entity_df[["locus", "sequence", "protein_id"]], how="inner", on=["locus", "sequence"])
# homodimer_uniprot_tair_df[homodimer_uniprot_tair_df['protein_id'].isna()]
homodimer_uniprot_tair_df = homodimer_uniprot_tair_df.drop_duplicates(subset=["locus", "sequence"], keep='first')




# # filter out proteins in tair df that also in uniprot
# uniprot_list_extra = list(set(athan_uniprot_df[athan_uniprot_df["Reviewed"]=="reviewed"]["TAIR"].tolist()))
# uniprot_list = [str(x)[:-1] for x in uniprot_list_extra]
# uniprot_tair_df = entity_df[entity_df["locus"].isin(uniprot_list)]
# len(uniprot_tair_df)


# # filter entity_df using mmseqs list
# mmseqs_lst = list(set(read_lst(mmseqs_input_path)))
# print(len(mmseqs_lst))
# mmseqs_entity_df = entity_df[entity_df["protein_id"].isin(mmseqs_lst)]


json_list=[]
for index, row in homodimer_uniprot_tair_df.iterrows():
# for index, row in mmseqs_entity_df.iterrows():
    sequence = row["sequence"]
    name = row["protein_id"]
   
    sequence_dicts=[]
    
    sequence_dict = {
        "proteinChain":{
            "sequence": sequence,
            "count": 1
        }
    }
    sequence_dicts+=[sequence_dict]
        
    protein_dict={}
    protein_dict["sequences"]=sequence_dicts
    protein_dict["name"]=name
    json_list+=[protein_dict]

# # write json file
print(f"Length of possible protein combination: {len(json_list)}")

### convert generating json format code into a function
with open(homodimer_output_path, "w") as json_file:
# with open(json_output_path, "w") as json_file:
    json.dump(json_list, json_file, indent=4)


# # TEMPORARY CODE: get the first 900 proteins of json_list
with open(json_900_output_path, "r") as f:
    data = json.load(f)

# json_900 = data[:900]

# with open(json_900_output_path, "w") as json_file:
#     json.dump(json_900, json_file, indent=4)

names=[]
for d in data:
    name = d["name"]
    names += [name]
print(len(names))

# print(len(json_900))
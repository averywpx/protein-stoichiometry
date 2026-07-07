import pandas as pd
from Bio import SeqIO
import json

arabidopsis_fa_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/raw_data/Arabidopsis/Athaliana_447_Araport11.protein.fa"
athan_short_sequence_fa_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/raw_data/Arabidopsis/Athaliana_447_Araport11_short.protein.fa"
mmseqs_input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/mmseqs_list/seq_id_less_than_0.5_athan.list"
entity_df_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/tair_arath_df.csv"
json_output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/athan_short_protein_complexes.json"

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

df = pd.read_csv(entity_df_output_path)

# filter df using mmseqs list
mmseqs_lst = list(set(read_lst(mmseqs_input_path)))
print(len(mmseqs_lst))
mmseqs_df = df[df["protein_id"].isin(mmseqs_lst)]

json_list=[]
for index, row in mmseqs_df.iterrows():
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

with open(json_output_path, "w") as json_file:
    json.dump(json_list, json_file, indent=4)



# {
#         "sequences": [
#             {
#                 "proteinChain": {
#                     "sequence": "MVREKVKVSTRTLQWKCVESKRDSKRLYYGRFILSPLMKGQADTIGIAMRRALLGEIEGTCITRAKSENIPHDYSNIAGIQESVHEILMNLNEIVLRSNLYGTRNALICVQGPGYITARDIILPPAVEIIDNTQHIATLTEPIDLCIELKIERNRGYSLKMSNNFEDRSYPIDAVFMPVENANHSIHSYGNGNEKQEILFLEIWTNGSLTPKEALHQASRNLINLFIPFLHVEEETFYLENNQHQVTLPFFPFHNRLVNLRKKKKTKELAFQYIFIDQLELPPRIYNCLKKSNIHTLLDLLNNSQEDLIKIEHFHVEDVKKILDILEKK",
#                     "count": 1
#                 }
#             }
#         ],
#         "name": "ATCG00740.1"
#     },
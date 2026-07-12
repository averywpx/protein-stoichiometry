import json
import copy
import random
from tqdm import tqdm

# # for training dataset
# A_input_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/homomeric_protein_complexes_similarity_less_than_0.5-add-msa.json"
# output_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/protenix_homomeric_complex.json"

# AB_input_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AB-add-msa.json"
# sequence_identity_input_id_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/seq_id_less_than_0.5_AAB.list"
# output_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_training_AAB.json"



# for valid dataset
# A_input_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/homomeric_protein_complexes_valid_dataset-add-msa.json"
# output_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_homomeric_complex.json"
# for valid dataset AAB
# AB_input_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AB_valid_data-add-msa.json"
# output_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_AAB_complex.json"

# for athan proteins
input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_with_msa/athan_900_short_protein_complexes-update-msa.json"
output_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_input_json/protenix_athan_900_mixed_proteins.json"

AMINO_ACID_LEN_LIMIT = 1000

def expand_possible_stoi(s_lens):
    possible_combinations=[]
    
    if len(s_lens) == 1: 
        size = AMINO_ACID_LEN_LIMIT//s_lens[0]
        for i in range(size):
            possible_combinations+=[[i+1]]
    elif len(s_lens) == 2:
        a_size = (AMINO_ACID_LEN_LIMIT-s_lens[1])//s_lens[0]
        b_size = (AMINO_ACID_LEN_LIMIT-s_lens[0])//s_lens[1]
        for i in range(a_size):
            for j in range(b_size):
                ac_len = (i+1)*s_lens[0] + (j+1)*s_lens[1]
                if ac_len < AMINO_ACID_LEN_LIMIT:
                    possible_combinations+=[[i+1,j+1]]
    return possible_combinations


# with open(A_input_path, "r") as file:
#     protein_list_A = json.load(file)
#     print(len(protein_list_A))


# ### WARNING: there are some As in this list
# with open(AB_input_path, "r") as file:
#     protein_list_AB = json.load(file)

# protein_list = protein_list_A + protein_list_AB
# total_proteins = len(protein_list)
# print(f"Before: {total_proteins}")

with open(input_path, "r") as file:
    protein_list = json.load(file)
    print(len(protein_list))

total_proteins = len(protein_list)
print(f"Before: {total_proteins}")


# with open(sequence_identity_input_id_path,"r") as file:
#     raw_less_similar_sequence_id = [line.strip()[1:-2] for line in file]
#     less_similar_sequence_id = list(set(raw_less_similar_sequence_id))
#     print(f"Sequence identity filter: {len(less_similar_sequence_id)}")





result_list = []
count=0
for p in tqdm(protein_list, total=total_proteins):
    # if count < 1000:
    sequences_dict = p["sequences"]
    sequences=[]
    # msas=[]
    paired_msa_paths=[]
    unpaired_msa_paths=[]
    for s in sequences_dict:
        sequence = s["proteinChain"]["sequence"]
        # msa=s["proteinChain"]["msa"]
        paired_msa_path=s["proteinChain"]["pairedMsaPath"]
        unpaired_msa_path=s["proteinChain"]["unpairedMsaPath"]

        sequences+=[sequence]
        paired_msa_paths+=[paired_msa_path]
        unpaired_msa_paths+=[unpaired_msa_path]
        # msas+=[msa]

    # Estimate if there are other possible stoichiometry
    # sequence = p["sequences"][0]["proteinChain"]["sequence"]
    name = p["name"]
    # s_len = len(sequence)
    # msa = p["sequences"][0]["proteinChain"]["msa"]
    # possible_combinations = 1000//s_len
    s_lens = [len(s) for s in sequences]
    possible_combinations = expand_possible_stoi(s_lens)
    # if len(possible_combinations) > 1 and name in less_similar_sequence_id:
    if len(possible_combinations) > 1:
        count+=1
        
        for pc in possible_combinations:
            if len(pc) == 1:
                
                order=pc[0]
                new_dict={}
                # new_dict["sequences"]=[
                #     {
                #         "proteinChain":{
                #             "sequence": sequences[0],
                #             "count": order,
                #             "msa": msas[0]
                #         }
                #     }
                # ]
                new_dict["sequences"]=[
                    {
                        "proteinChain":{
                            "sequence": sequences[0],
                            "count": order,
                            "pairedMsaPath": paired_msa_paths[0],
                            "unpairedMsaPath": unpaired_msa_paths[0]
                        }
                    }
                ]
                new_dict["name"] = f"{name}_{order}"
                # print(new_dict)
                result_list += [new_dict]
            elif len(pc) == 2:
                count_a = pc[0]
                count_b = pc[1]
                new_dict={}
                new_dict["sequences"]=[
                    {
                        "proteinChain":{
                            "sequence": sequences[0],
                            "count": count_a,
                            "msa": msas[0]
                        }
                    },
                    {
                        "proteinChain":{
                            "sequence": sequences[1],
                            "count": count_b,
                            "msa": msas[1]
                        }
                    }
                ]
                new_dict["name"] = f"{name}_{count_a}_{count_b}"
                # print(new_dict)
                result_list += [new_dict]

    # if possible_combinations > 1 and name in less_similar_sequence_id:
    #     count+=1
    #     p["name"] = f"{name}_1"
    #     result_list+=[p]
    #     for i in range(possible_combinations-1):
    #         order = i+2
    #         new_dict={}
    #         new_dict["sequences"]=[
    #             {
    #                 "proteinChain":{
    #                     "sequence": sequence,
    #                     "count": order,
    #                     "msa": msa
    #                 }
    #             }
    #         ]
    #         new_dict["name"] = f"{name}_{order}"
    #         # print(new_dict)
    #         result_list += [new_dict]

print(f"Number of Protein: {count}")
print(f"Number of Possible Combination: {len(result_list)}")
# random.shuffle(protein_list)
with open(output_path, "w") as f:
    json.dump(result_list, f, indent=4)


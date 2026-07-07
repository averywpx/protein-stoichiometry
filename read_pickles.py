import pickle
import pandas as pd
import json

DATA_TYPE = [
    # "casp16"
    # "train_data",
    "valid_data",
    # "test_data",
]

LARGER_THAN_3000 = [
    "A2",
    "A1B1",
    "A4",
    "A3",
    "A1B1C1",
    "A6",
]

TASK = [
    "analyze data",
    "generate json",
    "generate fasta",
]

# for input files
# input_file_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_raw_data/train_data.pkl"
input_file_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_raw_data/train_data.pkl"

# for homomeric complexes in training data
# fasta_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/homomeric_protein_complexes.fasta"
# for AAB training data
# fasta_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AAB.fasta"
### May not be used; for AAB valid data
# fasta_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AAB_valid_data.fasta"


# # for homomeric complexes in training data
# sequence_identity_input_id_homo_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/seq_id_less_than_0.5.list"
# sequence_identity_input_id_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/seq_id_less_than_0.5_AAB.list"



# # for training dataset
# json_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/homomeric_protein_complexes_similarity_less_than_0.5.json"
# for homomeric protein valid dataset
valid_data_homo_json_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_intermediate_results/homomeric_protein_complexes_valid_dataset.json"
# # for training dataset AB
json_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AB.json"
# # for valid dataset AB
json_output_path="/lustre/grp/gyqlab/wangpx/data/StoPred_data/protein_complexes_AB_valid_data.json"


def get_max_series(df, drop_columns):
    '''
    input: df, drop_columns
    output: df
    '''

    max_series = df.max().drop(labels=drop_columns)
    max_series = max_series.dropna()
    max_df = pd.DataFrame({"order of subunits": max_series.index, "maxinum copy number of a single subunit": max_series.values}) 
    return max_df

def get_counts_and_percentage(df, size):
    count_series = df["counts"].value_counts()
    summary_df = pd.DataFrame({"number of subunits": count_series.index, "number of subunit combinations": count_series.values})
    summary_df["percent of subunit combinations"] = summary_df["number of subunit combinations"]/size
    return summary_df

# with open("/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_raw_data/valid_data.pkl", 'rb') as f:
#     raw_data = f.read(10000) # Read a sample of the file
#     result = chardet.detect(raw_data)
#     encoding = result['encoding']
#     print(f"Detected encoding: {encoding}")

task = "analyze data"

for dp in DATA_TYPE:

    # Read pkl file
    with open(input_file_path, "rb") as f:
        input_dict=pickle.load(f)
            
    # Convert dicts to df
    input_dict_list = []
    entity_count__dict_list = []
    # count = 0
    for k,v in input_dict.items():
        # if count <= 50:
        #     # print(f"Value: {v}\n")
        #     count+=1
        input_dict_list.append(v)
        count_dict = v["entity_count"]
        amino_acid_length = 0
        dates=[]
        sequences=[]
        db_codes=[]
        pdbx_db_accessions=[]
        for order, number in count_dict.items():
            individual_sequence = v[order]["sequence"]
            individual_db_code = v[order]["db_code"]
            individual_pdbx_db_accession = v[order]["pdbx_db_accession"]
            amino_acid_length += number*len(individual_sequence)
            sequences += [individual_sequence]
            db_codes += [individual_db_code]
            pdbx_db_accessions += [individual_pdbx_db_accession]
        count_dict["amino acid length"] = amino_acid_length
        count_dict["release_date"]=v["release_date"]
        count_dict["stoichiometry"] = v["stoichiometry"]
        
        count_dict["sequences"] = sequences
        count_dict["db_codes"] = db_codes
        count_dict["pdbx_db_accessions"]  = pdbx_db_accessions
        count_dict["name"] = v["unique_id"]
        # count_dict["unique_id"] = v["unique_id"]
        entity_count__dict_list.append(count_dict)


    entity_count_df = pd.DataFrame.from_dict(entity_count__dict_list)
    
    # Simple data analysis
    entity_count_df["counts"] = entity_count_df.count(axis="columns", numeric_only=True)-1
    entity_count_df.to_csv("/lustre/grp/gyqlab/wangpx/data/StoPred_data/train_data_entity_count_tax_df.csv", index=False)
    
    # Limit date to before 9-30-2021
    entity_count_df['release_date'] = pd.to_datetime(entity_count_df['release_date'])
    entity_count_df = entity_count_df[entity_count_df["release_date"]> '2021-09-30']
    entity_count_df.to_csv("/lustre/grp/gyqlab/wangpx/data/StoPred_data/train_data_entity_count_tax_df_after_20210930.csv", index=False)


    # Limit number of subunits to be less than or equal to 3
    entity_count_df = entity_count_df[entity_count_df["counts"]<=3]
    size = len(entity_count_df)
    print(entity_count_df)
    print(entity_count_df["stoichiometry"].value_counts())

        
    # if task == "analyze data":
        
    #     # Separate entity df based on stoichiometry counts
    #     ac_more_than_3000 = entity_count_df[entity_count_df["amino acid length"]>3000]
    #     ac_less_than_3000 = entity_count_df[entity_count_df["amino acid length"]<=3000]
    #     ac_more_than_3000_size = len(ac_more_than_3000)
    #     ac_less_than_3000_size = len(ac_less_than_3000)
        
    #     # count number of subunits
    #     ac_more_than_3000_summary_df = get_counts_and_percentage(ac_more_than_3000, ac_more_than_3000_size)
    #     ac_less_than_3000_summary_df = get_counts_and_percentage(ac_less_than_3000, ac_less_than_3000_size)

    #     # Generate summary of counts of stoichiometry
    #     ac_more_than_3000_stoi_series = ac_more_than_3000["stoichiometry"].value_counts()
    #     ac_less_than_3000_stoi_series = ac_less_than_3000["stoichiometry"].value_counts()
    #     stoi_df_x = pd.DataFrame({"stoichiometry": ac_more_than_3000_stoi_series.index, "counts of amino acid length>3000": ac_more_than_3000_stoi_series.values})
    #     stoi_df = pd.DataFrame({"stoichiometry": ac_less_than_3000_stoi_series.index, "counts of amino acid length<=3000": ac_less_than_3000_stoi_series.values})
    #     stoi_df = stoi_df.merge(stoi_df_x, on="stoichiometry", how="outer")
    #     stoi_df.to_csv(f"{dp}_amino_acid_len_3000_split_stoichiometry_summary.csv", sep="\t")
    #     # print(len(ac_more_than_3000_stoi_series))
    #     # print(len(ac_less_than_3000_stoi_series))
    #     # total_len = len(entity_count_df["stoichiometry"].value_counts())
    #     # print(f"Total len: {total_len}")


    #     # # Count proteins having a single subunit
    #     # single_subunit = len(entity_count_df[entity_count_df["stoichiometry"]=="A1"])
    #     # print(f"Number of proteins with A1 stoichiometry: {single_subunit}")
    #     # print(f"Percent of proteins with A1 stoichiometry: {single_subunit/len(entity_count_df)}")

    
    #     # count maximum number of the copy number of a single subunit
    #     ac_more_than_3000_max_df = get_max_series(ac_more_than_3000, drop_columns=["counts", "stoichiometry", "amino acid length"]) 
    #     ac_less_than_3000_max_df = get_max_series(ac_less_than_3000, drop_columns=["counts", "stoichiometry", "amino acid length"])

    #     print(f"================================================= Summary of {dp} with subunits <=3 =================================================")
    #     print(f"{dp} data size: {size}\n")
        
    #     print(f"===================================== Summary of {dp} with amino acid length larger than 3000 ====================================")
    #     print(f"Size: {ac_more_than_3000_size}")
    #     print(ac_more_than_3000_summary_df)
    #     print("\n")
    #     print(ac_more_than_3000_max_df)
    #     print("\n")
        
    #     print(f"===================================== Summary of {dp} with amino acid length less than 3000 ====================================")
    #     print(f"Size: {ac_less_than_3000_size}")
    #     print(ac_less_than_3000_summary_df)
    #     print("\n")
    #     print(ac_less_than_3000_max_df)
  
    #     complex_df = entity_count_df[entity_count_df["counts"]==1]
    #     print(f"Length of entity_count_df: {len(entity_count_df)}")
    #     print(f"Length of homomeric complex: {len(complex_df)}")

    elif task == "generate fasta":
        json_list = []
        fasta_data = ""
        # print(entity_count_df)
        complex_df = entity_count_df[entity_count_df["counts"]<=2]
        print(f"Length of complex df :{len(complex_df)}")
        # ave_sequence_len = complex_df["amino acid length"].mean()
        # print(f"Average length of sequence :{ave_sequence_len}")
        for index, row in complex_df.iterrows():
            sequences = row["sequences"]
            name = row["name"]
            
            for idx, s in enumerate(sequences):
                if idx == 0:
                    data = ">"+name+"_A"+"\n"+s+"\n"
                    fasta_data+=data
                elif idx == 1:
                    data = ">"+name+"_B"+"\n"+s+"\n"
                    fasta_data+=data

            # sequence_length = row["amino acid length"]
            # possible_combinations = 1000//sequence_length
            # for i in range(possible_combinations):
            #     sequence_dict={}
            #     sequence_dict["sequences"]=[
            #         {
            #             "proteinChain":{
            #                 "sequence": sequence,
            #                 "count": i+1
            #             }
            #         }
            #     ]
            #     sequence_dict["name"]=f"{name}_{i+1}"
            #     json_list+=[sequence_dict]
            # generate content of fasta file
            
        
        # write fasta file
        with open(fasta_output_path, "wt") as fasta_file:
            fasta_file.write(fasta_data)
        # print(f"Length of possible protein combination: {len(json_list)}")
        # with open(json_output_path, "w") as json_file:
        #     json.dump(json_list, json_file, indent=4)
    else:
        # with open(sequence_identity_input_id_path,"r") as file:
        #     raw_less_similar_sequence_id = [line.strip()[1:-2] for line in file]
        #     less_similar_sequence_id = list(set(raw_less_similar_sequence_id))
        #     print(f"Sequence identity filter: {len(less_similar_sequence_id)}")
            
        # with open(sequence_identity_input_id_homo_path,"r") as file:
        #     less_similar_sequence_id_homo = [line.strip()[1:] for line in file]
        #     print(f"Sequence identity filter (homo): {len(less_similar_sequence_id_homo)}")

        with open(valid_data_homo_json_output_path, "r") as file:
            raw_protein_list = json.load(file)
            less_similar_sequence_id_A=[]
            for d in raw_protein_list:
                name = d["name"]
                less_similar_sequence_id_A+=[name]
            print(f"Sequence identity filter: {len(less_similar_sequence_id_A)}")

            
        json_list = []
        id_counts=0

        complex_df = entity_count_df[entity_count_df["counts"]<=2]
        print(f"Length of complex df :{len(complex_df)}")
        # print(f"Number of proteins sequence with similarity lower than 0.5: {len(less_similar_sequence_id)}")
        ave_sequence_len = complex_df["amino acid length"].mean()
        print(f"Average length of sequence :{ave_sequence_len}")


        for index, row in complex_df.iterrows():
            sequences = row["sequences"]
            name = row["name"]
            
            # if name in less_similar_sequence_id and name not in less_similar_sequence_id_homo:
            if name not in less_similar_sequence_id_A:
                # sequence_length = row["amino acid length"]
                # possible_combinations = 1000//sequence_length
                # for i in range(possible_combinations):
                sequence_dicts=[]
                for s in sequences:
                    sequence_dict = {
                        "proteinChain":{
                            "sequence": s,
                            "count": 1
                        }
                    }
                    sequence_dicts+=[sequence_dict]
                
                protein_dict={}
                protein_dict["sequences"]=sequence_dicts
                protein_dict["name"]=name
                json_list+=[protein_dict]
                # id_counts+=1
        # print(f"Number of proteins with similarity lower than 0.5:{id_counts}")
            
        # # write json file
        print(f"Length of possible protein combination: {len(json_list)}")
        with open(json_output_path, "w") as json_file:
            json.dump(json_list, json_file, indent=4)
    


# intermediate_dict = entity_count_df.count().to_dict()
# intermediate_df = entity_count_df[(entity_count_df["2"]==780)]
# print(intermediate_df)
# print(input_dict["8OLB_1"])
# not_na_14 = intermediate_df["unique_id"].tolist()

# for k in not_na_14:
#     not_na_14_dict = input_dict[k]
#     print(not_na_14_dict)
# sorted_intermediate_dict = dict(sorted(intermediate_dict.items()))
# print(sorted_intermediate_dict)

# summery_dict={}
# last_count=0
# for i in range(len(sorted_intermediate_dict),0,-1):
#     v=sorted_intermediate_dict[str(i)]
#     print(f"v:{v}")
#     print(f"last_count: {last_count}")
#     summery_dict[i]=v-last_count
#     last_count=v

# print(summery_dict)

# result_dict = {}
# last_count = 0
# for i in range(len(entity_count_df.columns),0,-1):



# print(input_df.head(10))
# print(input_df["entity_count"].head(20))
# print(input_df["stoichiometry"].value_counts())
# print(type(input_dict_list))


# count=1

        
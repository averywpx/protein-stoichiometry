import json
import subprocess

# wc -l == 6739
START_INDEX=6737
DATA_TYPE="homodimer_athan_mixed_v0.5.0"

# input_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_training_AAB.json"

# For athan proteins
input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_input_json/protenix_homodimer_athan_mixed_proteins.json"

with open(input_path, "r") as file:
    unrun_protein_list = json.load(file)

# print(unrun_protein_list[0])
# print(unrun_protein_list[-1])

# run_protein_list = protein_list[:START_INDEX]
# print(f"Order: 1")
# print(run_protein_list[0])
# print(run_protein_list[-1])
# with open(f"/lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_homomeric_complex_json/protenix_homomeric_complex_1.json", "w") as f:
#     json.dump(run_protein_list, f, indent=4)

# unrun_protein_list = protein_list[START_INDEX:]


chunk_number = 21
chunk_size = len(unrun_protein_list)//chunk_number

chunk_list = []

for i in range(chunk_number+1):
    order = i+1
    # if i != chunk_size-1:
    protein_list_chunk = unrun_protein_list[i*chunk_size:(i+1)*chunk_size]
    print(f"Order: {order}")
    # print(protein_list_chunk[0])
    # print(protein_list_chunk[-1])
    p_len = len(protein_list_chunk)
    # print(p_len)
    # Generate sliced jsons
    with open(f"/storage/gaoyiqinLab/wangpeixin/work/protenix_sh_scripts/protenix_homodiemr_athan_mixed_{order}.json", "w") as f:
        json.dump(protein_list_chunk, f, indent=4)
        
    # else:
        # protein_list_chunk = unrun_protein_list[i*chunk_size:]
        # print(f"Order: {order}")
        # print(protein_list_chunk[0])
        # print(protein_list_chunk[-1])
        
        # with open(f"/lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_homomeric_complex_{order}.json", "w") as f:
        #     json.dump(protein_list_chunk, f, indent=4)

    # submit jobs
    result = subprocess.run(["bash", "/storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/submit_protenix_job.sh", DATA_TYPE, str(order)], capture_output=True, text=True)
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)
    print("Return code:", result.returncode)

    


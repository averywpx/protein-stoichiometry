#!/bin/bash

JOB_ID=$1 
TYPE_ID=$2

echo "#!/bin/bash" > /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH -o job.protenix.$JOB_ID.out" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH -e job.protenix.$JOB_ID.err" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH --gres=gpu:1" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH -p gaoyiqinlab" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH --qos=normal" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH -J $JOB_ID.protenix" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "#SBATCH --nodes=1" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh

echo "source /storage/gaoyiqinLab/wangpeixin/.bashrc" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "conda activate protenix" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh
echo "cd /storage/gaoyiqinLab/wangpeixin/protenix" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh


## train data
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_homomeric_complex_json/protenix_homomeric_complex_$JOB_ID.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_$JOB_ID.sh

# valid data
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_homomeric_complex.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_data --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_$JOB_ID.sh

# # valid data AAB
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_AAB_complex.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_AAB --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh

# # train data AAB
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_training_AAB_json/protenix_training_AAB_$JOB_ID.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_training_AAB_2 --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh

# test athan
echo "~/anaconda3/envs/protenix/bin/protenix pred --input /storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/test_msa-update-msa.json --out_dir /storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_output/base_1_output_test_athan --seeds 101 --model_name "protenix_base_default_v0.5.0" --use_default_params true" >> /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh


# #submit the job
# sbatch /storage/gaoyiqinLab/wangpeixin/scripts/protein-stoichiometry/sh_scripts/protenix_job_${TYPE_ID}_${JOB_ID}.sh

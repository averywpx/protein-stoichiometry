#!/bin/bash
#SBATCH -o job.protenix.test.out
#SBATCH -e job.protenix.test.err
#SBATCH --gres=gpu:1
#SBATCH -p gaoyiqinlab
#SBATCH --qos=normal
#SBATCH -J test.protenix
#SBATCH --nodes=1
source /storage/gaoyiqinLab/wangpeixin/.bashrc
conda activate protenix
cd /storage/gaoyiqinLab/wangpeixin/protenix
~/anaconda3/envs/protenix/bin/protenix pred --input /storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/json_without_msa/test_msa-update-msa.json --out_dir /storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_output/base_1_output_test_athan --seeds 101 --model_name protenix_base_default_v0.5.0 --use_default_params true

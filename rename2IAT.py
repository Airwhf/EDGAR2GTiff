#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2023/4/15 17:15
# @Author    :Haofan Wang
# @Email     :wanghf58@mail2.sysu.edu.cn
import glob
import os.path
import re
import shutil
import tqdm

if __name__ == "__main__":
    print("This script is written by Haofan Wang.")
    input_dir = r"D:\Emission-Inventory\EDGAR\GTiff"
    output_dir = r"D:\Emission-Inventory\EDGAR\GTiff4IAT_year"

    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)

    label = "EDGARv6.1"

    files = glob.glob(f"{input_dir}/*.tiff")

    for file in tqdm.tqdm(files):
        file_name = os.path.basename(file)
        # Get the species name from file name.
        # condition = f"(.*?)_(.*?)_(.*?)__(.*?)__(.*?).tiff"
        condition = "EDGARv6.1_(.*?)_(.*?)_(.*?).0.1x0.1.nc_t_year.tiff"
        encode_name = re.findall(condition, file_name)[0]
        pollutant = encode_name[0]
        year = encode_name[1]
        sector = encode_name[2]

        new_name = f"{label}_{year}_00__{sector}__{pollutant}.tiff"
        output_name = f"{output_dir}/{new_name}"
        shutil.copy(file, output_name)

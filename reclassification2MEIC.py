#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2023/4/17 14:28
# @Author    :Haofan Wang
# @Email     :wanghf58@mail2.sysu.edu.cn
import glob
import os.path

import numpy as np
import rasterio

if __name__ == "__main__":
    reclassification = {
        "transportation": ["TNR_Aviation_CDS", "TNR_Aviation_CRS", "TNR_Aviation_LTO", "TNR_Aviation_SPS", "TRO_noRES",
                           "TRO_RES", "TNR_Other", "TNR_Ship"],
        "power": ["ENE"],
        "residential": ["RCO", "SWD_INC", "FOO_PAP", "SWD_LDF"],
        "industry": ["REF_TRF", "IND", "FFF", "PRO", "NMM", "CHE", "IRO", "NFE", "NEU", "PRU_SOL", "WWT"],
        "agriculture": ["MNM", "AWB", "AGS"]
    }

    input_dir = r"D:\Emission-Inventory\EDGAR\GTiff4IAT_year"
    output_dir = r"D:\Emission-Inventory\EDGAR\GTiff4IAT_year_reclassification"

    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)

    pollutants = ["BC", "CO", "NH3", "NMVOC", "NOx", "PM2.5", "PM10", "SO2", "OC"]

    years = np.arange(1970, 2019, 1)
    for year in years:
        for key in reclassification.keys():
            for pollutant in pollutants:

                output_name = f"{output_dir}/EDGARv6.4_{year}_00__{key}__{pollutant}.tiff"
                if os.path.exists(output_name):
                    continue
                    
                sectors = reclassification[key]
                files = []  # File for pollutant.
                for sector in sectors:
                    file = glob.glob(f"{input_dir}/*_{year}_*__{sector}__{pollutant}.tiff")
                    if len(file) == 1:
                        files.append(file[0])

                result = np.zeros((1800, 3600))
                for file in files:
                    dataset = rasterio.open(file)
                    transform = dataset.transform
                    band = dataset.read(1)
                    result += band

                # 输出
                with rasterio.open(
                        output_name,
                        'w',
                        driver='GTiff',
                        height=result.shape[0],
                        width=result.shape[1],
                        count=1,
                        dtype=result.dtype,
                        crs='+proj=latlong',
                        transform=transform,
                ) as dst:
                    dst.write(result, 1)

                print(output_name)
   
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2023/4/15 15:48
# @Author    :Haofan Wang
# @Email     :wanghf58@mail2.sysu.edu.cn
import glob
import os.path

import rasterio
import xarray as xr
import pyproj


if __name__ == '__main__':

    input_dir = r"D:\Emission-Inventory\EDGAR"
    output_dir = r"D:\Emission-Inventory\EDGAR\GTiff"

    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)

    files = glob.glob(f"{input_dir}/*.nc")
    for file in files:
        # 定义WGS84等经纬度投影
        crs_proj = pyproj.CRS.from_string('EPSG:4326')

        # 读取NetCDF数据集
        ds = xr.open_dataset(file)

        sub_name = os.path.basename(file)

        # 获取所有数据变量列表
        variable = list(ds.data_vars.keys())[0]
        data_array = ds[variable]

        # 获取空间信息
        height, width = ds[variable].shape[0], ds[variable].shape[1]
        south, north = ds['lat'].values.max(), ds['lat'].values.min()
        west, east = ds['lon'].values.min(), ds['lon'].values.max()

        # 创建GTiff文件
        with rasterio.open(f'{output_dir}/{sub_name}_t_year.tiff', 'w', driver='GTiff',
                           width=width, height=height, count=1,
                           dtype=data_array.dtype.name, nodata=0,
                           transform=rasterio.transform.from_bounds(west, south, east, north, width, height),
                           crs=crs_proj) as dst:
            # 将NetCDF数据写入GTiff
            dst.write(data_array.values * 10000 * 10000 * 0.001 * 31536000, 1)
        print(f'{output_dir}/{sub_name}')

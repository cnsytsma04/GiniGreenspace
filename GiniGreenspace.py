import numpy as np
import pandas as pd
import geopandas as gpd
from typing import List
from pathlib import Path
from osgeo import gdal
from census import Census
from us import states

wd = Path.cwd()
print(wd)

inputs = wd / 'Inputs'
if not inputs.exists():
    inputs.mkdir()

impervious_cover_path = str(inputs) + "\\nlcd_2021_impervious_l48_20230630.img"
impervious_descriptor_path = str(inputs) + "\\nlcd_2021_impervious_descriptor_l48_20230630.img"
usa_parks_path = str(inputs) + "\\USA_Parks.shp"
parkserve_path = str(inputs) + "\\ParkServe_Parks.shp"

impervious_Cover = gdal.BuildVRT(destName= 'ImperviousCover.vrt', srcDSOrSrcDSTab= gdal.Open(impervious_cover_path))
impervious_Descriptor = gdal.BuildVRT(destName = 'ImperviousDescriptor.vrt', srcDSOrSrcDSTab=gdal.Open(impervious_descriptor_path))

with open('MyCensusAPI.txt', 'r') as file:
    census_api_key = file.read().replace('\n', '')
    c = Census(census_api_key)

va_df = pd.DataFrame(c.acs5.state_county_tract(fields = ("NAME","B01003_001E"),
                          state_fips = states.VA.fips,
                          county_fips = "*",
                          tract = "*",
                          year = 2021))
print(va_df.head(2))
print('Shape:', va_df.shape)
va_df["GEOID"] = va_df["state"] + va_df["county"] + va_df["tract"]
va_df = va_df.drop(columns = ["state","county","tract"])
print(va_df.head(2))

va_tract = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2021/TRACT/tl_2021_51_tract.zip")
print(va_tract.head(2))
print('Shape:', va_tract.shape)

va_merge = va_tract.merge(va_df, on = "GEOID")
print(va_merge.head(2))

#def euclidean_distance(x: float, y: float, df: DataFrame, acceptable_distance: float) -> DataFrame:
#    '''
#   Calculates the Euclidean distance between a point and dataframe of points.
#    Returns a dataframe of points within the acceptable distance.
#    
#    Args:
#        x: x-coordinate of point
#       y: y-coordinate of point
#        df: dataframe with x and y coords
#    
#   Returns:
#        df: dataframe of points within the acceptable distance
#    '''
#    df['distance'] = np.sqrt((x - df['x'])**2 + (y - df['y'])**2)
#    return df.loc[df['distance'] < acceptable_distance]

#example_data = DataFrame({'x': [1.0, 2.0, 3.0], 'y': [1.0, 2.0, 3.0]})
#df = euclidean_distance(1.0, 1.0, example_data, 2.0)
#print(example_data)
#print(df)
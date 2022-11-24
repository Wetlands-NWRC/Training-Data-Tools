import sys

import arcpy


arcpy.env.workspace = 'CURRENT'

TARGET = ''
LAND_COVER = ''

# check if in FC is in the right format to split
rows = [row[0] for row in arcpy.da.SearchCursor(TARGET, LAND_COVER)]
unique = set(rows)

is_dissolved = (len(rows) > len(unique))

if not is_dissolved:
    out_fc = f'{TARGET}_dis'
    arcpy.Dissolve_management(
        in_features=TARGET,
        out_feature_class=out_fc
    )




# set a tmp workspace to do all of the processing

# split the dissolved polygon into seperate feature classes

# iterate over each of the feature classes

# specify a sampling paramaters i.e. min distance and number of points

# for each feature class try to generate random points with the input paramater specified above

# for each sample insert a column called land_cover, use field calc to insert land_cover type into FC


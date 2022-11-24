import sys

import arcpy


arcpy.env.workspace = 'CURRENT'

TARGET = ''
LAND_COVER = ''

# check if in FC is in the right format to split
rows = [row[0] for row in arcpy.da.SearchCursor(TARGET, LAND_COVER)]
land_covers = set(rows)

is_dissolved = (len(rows) > len(unique))

if not is_dissolved:
    out_fc = f'{TARGET}_dis'
    arcpy.Dissolve_management(
        in_features=TARGET,
        out_feature_class=out_fc
    )
    TARGET = out_fc

for land_cover in land_covers:
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=TARGET,
        selection_type='NEW_SELECTION',
        where_clause=f"[{LAND_COVER}] == '{land_cover}'"
    )


# iterate over each of the feature classes

# specify a sampling paramaters i.e. min distance and number of points

# for each feature class try to generate random points with the input paramater specified above

# for each sample insert a column called land_cover, use field calc to insert land_cover type into FC


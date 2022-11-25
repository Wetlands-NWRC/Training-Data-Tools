import os

import arcpy

cwd = os.getcwd()
arcpy.env.workspace = cwd
arcpy.env.overwriteOutput = True

print(f"arcpy.env.workspace: {arcpy.env.workspace}")

TARGET = 'training_data_un_dissolved'
LAND_COVER = 'land_cover'

# check if in FC is in the right format to split
rows = [row[0] for row in arcpy.da.SearchCursor(TARGET, LAND_COVER)]
land_covers = set(rows)

print(f"nRows = {len(rows)}")
print(f'nLand Covers = {len(land_covers)}')

is_dissolved = (len(rows) < len(land_covers))
print(f"Is Dissolved: {is_dissolved}")

if not is_dissolved:
    print(f"Dissolving: on {LAND_COVER}")
    out_fc = f'{TARGET}_dis'
    arcpy.Dissolve_management(
        in_features=TARGET,
        out_feature_class=out_fc
    )
    TARGET = out_fc
    print(f'Target Feature Class: {TARGET}')

print(f"{TARGET} is Dissolved... Proceeding to Point Generation")

for land_cover in land_covers:
    print(f"Selecting: {land_cover}")
    # log
    print(f"In layer = {TARGET}")
    print("selection_type = 'NEW_SELECTION'")

    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=TARGET,
        selection_type='NEW_SELECTION',
        where_clause=f"{LAND_COVER} == '{land_cover}'"
    )

    out_name = f'_{land_cover}_ran_pts'

    arcpy.CreateRandomPoints_management(
        in_table=out_name,
        out_path=None,
        constraining_feature_class=TARGET,
        number_of_points_or_field=1000,
        minimum_allowed_distance='25 Meters'
    )

    arcpy.CalculateField_management(
        in_table=out_name,
        field_type='SHORT',
        expression=f'{land_cover}',
        expression_type='PYTHON3',
        field='land_cover'
    )

    arcpy.SelectLayerByAttribute_management(TARGET, 'CLEAR_SELECTION')


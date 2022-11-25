import os

import arcpy

cwd = os.getcwd()
arcpy.env.workspace = cwd
arcpy.env.overwriteOutput = True
# print(f"{#<'Script Starts'}")
print(f"arcpy.env.workspace: {arcpy.env.workspace}")

TARGET = 'training_data_un_dissolved'
LAND_COVER = 'land_cover'

# check if in FC is in the right format to split
rows = [row[0] for row in arcpy.da.SearchCursor(TARGET, LAND_COVER)]
land_covers = set(rows)

print(f"\nnRows = {len(rows)}")
print(f'nLand Covers = {len(land_covers)}')

is_dissolved = (len(rows) < len(land_covers))
print(f"\nIs Dissolved: {is_dissolved}")

if not is_dissolved:
    print(f"Dissolving: on {LAND_COVER}")
    out_fc = f'{TARGET}_dis'
    arcpy.Dissolve_management(
        in_features=TARGET,
        out_feature_class=out_fc,
        dissolve_field=[LAND_COVER]
    )
    TARGET = out_fc
    print(f'Target Feature Class: {TARGET}')

print(f"{TARGET} is Dissolved... Proceeding to Point Generation\n")

for land_cover in land_covers:
    ####################################################
    # tool paramaters
    in_layer = TARGET
    selection_ty = 'NEW_SELECTION'
    where = f"{LAND_COVER} = '{land_cover}'"

    print('Executing: Select Layer By Attribute Management')
    # logging
    print(f"In layer = {TARGET}")
    print(f"selection_type = {selection_ty}")
    print(f'where_clause ={where}')

    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=TARGET,
        selection_type=selection_ty,
        where_clause=where
    )
    print('GP Tool Exits...\n')
    ###################################################
    # tool pramaters
    out_name = f'_{land_cover}_ran_pts'
    out_path = arcpy.env.workspace
    bounding_fc = TARGET
    number_of_points = 1000
    min_allowed_distance = '25 Meters'

    # logging
    print('Executing: Create Random Points Management')
    # log
    print(f"out_name = {out_name}")
    print(f"out_path = {out_path}")
    print(f"constraining_feature_class = {bounding_fc}")
    print(f"number_of_points_or_field = {number_of_points}")
    print(f"minimum_allowed_distance = {min_allowed_distance}")

    arcpy.CreateRandomPoints_management(
        out_name=out_name,
        out_path=out_path,
        constraining_feature_class=TARGET,
        number_of_points_or_field=number_of_points,
        minimum_allowed_distance=min_allowed_distance
    )
    print("GP Tool Exits...\n")
    #################################################

    arcpy.CalculateField_management(
        in_table=out_name,
        field_type='SHORT',
        expression=f'{land_cover}',
        expression_type='PYTHON3',
        field='land_cover'
    )

    arcpy.SelectLayerByAttribute_management(TARGET, 'CLEAR_SELECTION')

    print(f'END: {land_cover}\n')
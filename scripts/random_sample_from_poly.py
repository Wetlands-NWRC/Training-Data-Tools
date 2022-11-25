import sys

import arcpy


arcpy.env.workspace = 'CURRENT'

TARGET = ''
LAND_COVER = ''

# check if in FC is in the right format to split
rows = [row[0] for row in arcpy.da.SearchCursor(TARGET, LAND_COVER)]
land_covers = set(rows)

is_dissolved = (len(rows) > len(land_covers))
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

for land_cover in land_covers:
    print(f"Selecting: {land_cover}")
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view=TARGET,
        selection_type='NEW_SELECTION',
        where_clause=f"[{LAND_COVER}] == '{land_cover}'"
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


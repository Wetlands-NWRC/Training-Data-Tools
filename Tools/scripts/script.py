from dataclasses import dataclass
from enum import Enum

import arcpy

arcpy.env.workspace = "CURRENT"
arcpy.env.overwriteOutput = True

OUT_GDB = r"C:\Users\rhamilton\projects\FPCA\SK\ST_DENIS\DATA\GDB\tmp.gdb"

# get the unique land covers from the input


for val in [1, 2]:
    arcpy.SelectLayerByAttribute_management(
        in_layer_or_view="std_tmp_perm_intersect_Disso",
        where_clause=f'value = {val}'
    )

    out_name = f'_{val}_ran_pts'

    arcpy.CreateRandomPoints_management(
        out_path=OUT_GDB,
        out_name=out_name,
        constraining_feature_class="std_tmp_perm_intersect_Disso",
        number_of_points_or_field=1000,
        minimum_allowed_distance="25 Meters"
    )

    arcpy.CalculateField_management(
        in_table=out_name,
        field='land_cover',
        expression=f'{val}',
        expression_type='PYTHON3',
        field_type='SHORT'
    )

    arcpy.SelectLayerByAttribute_management(
        "std_tmp_perm_intersect_Disso", 'CLEAR_SELECTION')

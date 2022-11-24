import arcpy


arcpy.env.workspace = 'CURRENT'

# check if dissolved i.e. if the length of the uniq land_cover is less than the number of rows

# if not dissolved, dissolve on the land_cover column

# set a tmp workspace to do all of the processing

# split the dissolved polygon into seperate feature classes

# iterate over each of the feature classes

# specify a sampling paramaters i.e. min distance and number of points

# for each feature class try to generate random points with the input paramater specified above

# for each sample insert a column called land_cover, use field calc to insert land_cover type into FC


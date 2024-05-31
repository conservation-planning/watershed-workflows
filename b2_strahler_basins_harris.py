# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   watershed-workflows: Strahler Basins (Harris)
#
#   name: b2_strahler_basins_harris.py
#   authors: Derrick Burt, Lake Willet, & Jeff Howarth
#   last modified: 5/31/2024
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

'''
*** DIRECTORY PATHS SHOULD BE MODIFIED BEFORE RUNNING SCRIPT ***

    The paths in this script are system dependent. 
    
    If you cloned the repository and are working on a windows os, 
    you should be able to execute the script by modifying the root 
    directorty (work variable).

    If your cloned the repository and are working on a Mac os, you
    will need to modify all subdirectorys by  
        1) removing raw string-literal operator "r"
        2) replacing r"path\to\dir" with "/"
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Import modules.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# Import tools from WBT module WBW module.

from WBT.whitebox_tools import WhiteboxTools

# Declare a name for tools.

wbt = WhiteboxTools()
 
# Set the Whitebox working directory.

work =  r"G:\My Drive\whitebox_basins" # Replace with path to root directory.

# Set working directory.

wbt.work_dir = work

# Declare a director for our inputs and outputs.  

input = work + r"\strahler_method"
out = work + r"\strahler_method\out_harris"

# Declare a name for our test data.

dem_harris = input + r"\in\DEM_level12_harris.tif"   
parcels = input + r"\in\parcel_study_region_Harris.shp"  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  1. FLOW ANALYSIS OF DEM
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# From DEM, create: (1) filled depressions, (2) flow dir, (3) and flow acc.

wbt.flow_accumulation_full_workflow(
    dem=dem_harris, 
    out_dem=out + r"\_01_filled_dep.tif", 
    out_pntr=out + r"\_02_flow_direction.tif", 
    out_accum=out + r"\_03_flow_accumulation.tif", 
    out_type="Specific Contributing Area", 
    log=False, 
    clip=False, 
    esri_pntr=False, 
    # callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  EXTRACT STREAM NETWORKS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# Extract streams from flow accumulation raster.

wbt.extract_streams(
    flow_accum = out + r"\_03_flow_accumulation.tif", 
    output = out + r"\_04_extracted_streams.tif", 
    threshold = 10000, 
    zero_background=False, 
    #callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   STREAM ORDER ANALYSIS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# Caclulate strahler order streams from flow direction and streams.

wbt.strahler_stream_order(
    d8_pntr = out + r"\_02_flow_direction.tif", 
    streams = out + r"\_04_extracted_streams.tif", 
    output = out + r"\_05_strahler_streams.tif", 
    esri_pntr=False, 
    zero_background=False, 
    #callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   STRAHLER BASIN CLASSIFICATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

'''

** THIS STEP SHOULD BE PERFORMED USING UNCLIPPED INPUTS **

    If we use clipped inputs for strahler_order_basins():
     
        the strahler basins are not properly created as 
        intersecting basins (that are not entirely within
        the parcel) are not properly calculated.
    

    The watershed() function, however, creates the same basins
    regardless of the order of operations:
        
        we can use clipped inputs, or inputs at the watershed 
        extent, and we will get the same basin areas.
 

'''

# Calculate watershed basins based on strahler order.

wbt.strahler_order_basins(
    d8_pntr = out + r"\_02_flow_direction.tif", 
    streams = out + r"\_05_strahler_streams.tif",
    output = out + r"\_10_strahler_basins.tif",
    esri_pntr=False,
    #callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#   CLIP BASINS, STREAMS, AND FLOW DIR TO PARCEL.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# Clip strahler basins to study region parcel.

wbt.clip_raster_to_polygon(
    i = out + r"\_10_strahler_basins.tif", 
    polygons = parcels, 
    output = out + r"\_10_strahler_basins_harris.tif", 
    maintain_dimensions=False, 
    #callback=default_callback
)

# Clip strahler streams to study region parcel.

wbt.clip_raster_to_polygon(
    i = out + r"\_05_strahler_streams.tif", 
    polygons = parcels, 
    output = out + r"\_05_strahler_streams_harris.tif", 
    maintain_dimensions=False, 
    #callback=default_callback
)

# Clip flow direction to parcels.

wbt.clip_raster_to_polygon(
    i = out + r"\_02_flow_direction.tif", 
    polygons = parcels, 
    output = out + r"\_02_flow_direction_harris.tif", 
    maintain_dimensions=False, 
    #callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#   VECTORIZE BASINS AND STREAMS.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 


# Convert clipped basins to vector layer.

wbt.raster_to_vector_polygons(
    i = out + r"\_10_strahler_basins_harris.tif", 
    output = out + r"\_12_VECTOR_strahler_basins_harris.shp", 
    #callback=default_callback
)

# Convert strahler streams to vector layer.

wbt.raster_streams_to_vector(
    streams = out + r"\_05_strahler_streams_harris.tif", 
    d8_pntr = out + r"\_02_flow_direction_harris.tif", 
    output = out + r"\_12_VECTOR_streams_harris.shp", 
    esri_pntr=False, 
    #all_vertices=False, 
    #callback=default_callback
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#  SELECT BASINS OF INTEREST IN QGIS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

'''

** THIS STEP SHOULD BE PERFORMED IN QGIS UNTIL wbt.extract_by_attribute() bug is resolved **

'''

# wbt.extract_by_attribute(
#     i = out + r"\_12_VECTOR_strahler_basins_sabourin.shp",
#     output = out + r"\_14_strahler_basins_extracted.shp",
#     statement = "VALUE==2.0000"
# )


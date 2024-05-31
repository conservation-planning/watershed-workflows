# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   watershed-workflows: Watershed Basins (Harris)
#
#   name: a2_strahler_basins_harris.py
#   authors: Lake Willet
#   last modified: 5/31/2024
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Import modules.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# Import tools from WBT module WBW module.
from WBT.whitebox_tools import WhiteboxTools
wbt = WhiteboxTools()
 
# Set the Whitebox working directory.
work =  r"G:\My Drive\whitebox_basins"

# Set working directory.
wbt.work_dir = work

# Declare a director for our inputs and outputs.  
input = work + r"\watershed_method"
out = work + r"\watershed_method\out_harris"


# Declare a name for our test data.
dem_harris = input + r"\in\DEM_level12_harris.tif"   
parcels = input + r"\in\parcel_study_region_Harris.shp"  


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #   FLOW ANALYSIS OF DEM
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# # FLOW ACCUMULATION, FLOW DIRECTION
# # wbt.flow_accumulation_full_workflow(
# #     dem = dem_harris, 
# #     out_dem = out + r"\_01_filled_dep.tif", 
# #     out_pntr = out + r"\_02_flow_direction.tif", 
# #     out_accum = out + r"\_03_flow_accumulation.tif", 
# #     out_type = "Specific Contributing Area", 
# #     log=False, 
# #     clip=False, 
# #     esri_pntr=False, 
# #     # callback=default_callback
# # )


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #   EXTRACT STREAM NETWORKS
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# # EXTRACT STREAMS WITHIN WATERSHED REGION
# wbt.extract_streams(
#     flow_accum = out + r"\_03_flow_accumulation.tif", 
#     output = out + r"\_04_extracted_streams.tif", 
#     threshold = 10000, 
#     zero_background = False, 
#     #callback=default_callback
# )

# # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # #   STREAM ORDER ANALYSIS
# # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# ## STRAHLER ORDER STREAMS WITHIN WATERSHED REGION
# wbt.strahler_stream_order(
#     d8_pntr = out + r"\_02_flow_direction.tif", 
#     streams = out + r"\_04_extracted_streams.tif", 
#     output = out + r"\_05_strahler_streams.tif", 
#     esri_pntr = False, 
#     zero_background = False, 
#     #callback=default_callback
# )


# # # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # # #   CLIP OUTPUTS TO STUDY REGION (reduce computational effort)
# # # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# # CLIP RASTER TO POLYGON (strahler ordered stream network)
# wbt.clip_raster_to_polygon(
#     i = out + r"\_05_strahler_streams.tif", 
#     polygons = parcels, 
#     output = out + r"\_05_clipped_strahler_streams.tif", 
#     maintain_dimensions = False, 
#     #callback=default_callback
# )

# # CLIP RASTER TO POLYGON (flow direction/pointer)
# wbt.clip_raster_to_polygon(
#     i = out + r"\_02_flow_direction.tif", 
#     polygons = parcels, 
#     output = out + r"\_02_clipped_flow_direction.tif", 
#     maintain_dimensions = False, 
#     #callback=default_callback
# )



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   EXTRACT STREAM ORDERS OF INTEREST
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### Order X: lower order
### Order Y: higher order

# RASTER STREAMS TO VECTOR
# wbt.raster_streams_to_vector(
#     streams = out + r"\_05_clipped_strahler_streams.tif", 
#     d8_pntr = out + r"\_02_clipped_flow_direction.tif", 
#     output = out + r"\_12_VECTOR_streams_harris.shp", 
#     esri_pntr = False, 
#     #all_vertices=False, 
#     #callback=default_callback
# )


# # ------------ #
# #  In QGIS     #
# # ------------ #
# # EXTRACT ORDER X BY ATTRIBUTE --> .shp (export with name "_13_Q_OrderX.shp")
# # EXTRACT ORDER Y BY ATTRIBUTE --> .shp (export with name "_14_Q_OrderY.shp")



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   FIND POUR POINTS (VECTOR METHOD)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# LINE INTERSECTION (where orders of interest overlap)
wbt.line_intersections(
    input1 = out + r"\_14_Q_OrderY.shp", 
    input2 = out + r"\_13_Q_OrderX.shp", 
    output = out + r"\_15_XY_intersection.shp", 
    #callback=default_callback
)



## JENSON SNAP POUR POINTS (re-align pour points with stream networks)
wbt.jenson_snap_pour_points(
    pour_pts = out + r"\_15_XY_intersection.shp", 
    streams = out + r"\_04_extracted_streams.tif", 
    output = out + r"\_16_snapped_ppts.shp", 
    snap_dist = 10,  
    #callback=default_callback
)

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #   WATERSHED CLASSIFICATION
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# WATERSHED (based on pour points)
wbt.watershed(
    d8_pntr = out + r"\_02_clipped_flow_direction.tif", 
    pour_pts = out + r"\_16_snapped_ppts.shp", 
    output = out + r"\_17_watersheds_higherorder.tif", 
    esri_pntr=False, 
    #callback=default_callback
)

# ## RASTER TO VECTOR POLYGONS
wbt.raster_to_vector_polygons(
    i = out + r"\_17_watersheds_higherorder.tif", 
    output = out + r"\_18_VECTOR_watersheds_higherorder.shp", 
    #callback=default_callback
)


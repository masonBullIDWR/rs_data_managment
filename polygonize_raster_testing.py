#%%
'''This will create a mosaic of some images and then polygonize that raster. You can also do a single image and not a mosaic.'''
import rasterio
from rasterio.features import shapes
from rasterio.merge import merge
from rasterio.plot import show
import geopandas as gpd
from shapely.geometry import shape
import numpy as np

polygonized_raster_destination = "C:\\Users\\mason.bull\\OneDrive - State of Idaho\\Desktop\\Geoprocessing\\Data\\TV\\TV2023\\shp\\tv_2023_classification_masked_polygonized.gpkg"

#do you need to mosaic any rasters before polygonization?
need_mosaic = 'y'

if need_mosaic =='y':
    first_raster_to_mosaic = "C:\\Users\\mason.bull\\OneDrive - State of Idaho\\Desktop\\Geoprocessing\\Data\\TV\\TV2023\\rast\\tv_2023_classification_masked.tif"
    second_raster_to_mosaic = "N:\\IrrigatedLands\\EasternSnakePlainAquifer\\RandomForest_2023\\ForRelease\\ESPA 2023 Random Forest Land Classification V2 Final.tif"

    image_1 = rasterio.open(first_raster_to_mosaic)
    image_2 = rasterio.open(second_raster_to_mosaic)

    raster_to_polygonize, transform = merge([image_1, image_2])
else:
    raster_to_polygonize = "C:\\Users\\mason.bull\\OneDrive - State of Idaho\\Desktop\\Geoprocessing\\Data\\TV\\TV2023\\rast\\tv_2023_classification_masked.tif"

if type(raster_to_polygonize) == str:
    with rasterio.open(raster_to_polygonize) as src:
        image = src.read(1)
        mask = (image != 3).astype(np.uint8)

        results = (
            {'properties': 
                {'raster_value': v}, 
             'geometry': s}
            for (s, v) in shapes(image, connectivity= 4, mask = mask, transform=src.transform)
        )

        polygonized_raster_gdf = gpd.GeoDataFrame.from_features(list(results), crs=src.crs)
else:
    mask = (raster_to_polygonize != 3).astype(np.uint8)
    results = (
        {'properties': 
            {'raster_value': v}, 
         'geometry': s}
        for (s, v) in shapes(raster_to_polygonize, connectivity= 4, mask = mask, transform=transform)
    )
    polygonized_raster_gdf = gpd.GeoDataFrame.from_features(list(results), crs=image_1.crs)

polygonized_raster_gdf.to_file(polygonized_raster_destination, driver = 'GPKG')
try:
    full_polygon = gpd.GeoDataFrame(geometry=[polygonized_raster_gdf.geometry.union_all()], crs=src.crs)
except:
    full_polygon = gpd.GeoDataFrame(geometry=[polygonized_raster_gdf.geometry.union_all()], crs=image_1.crs)

outline_shp_destination = polygonized_raster_destination.split('.gpkg')[0]+'_outline.shp'
full_polygon.to_file(outline_shp_destination)
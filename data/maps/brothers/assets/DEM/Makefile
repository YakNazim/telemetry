# Original Filenames
INPUT = SRTM_Brothers

# STRM geotiff come in WGS84
SOURCE_PROJECTION=EPSG:4326

# Hillshade options
AZIMUTH=330
ALTITUDE=85
EXAGERATE=4

# Color relief options
RAMP=colorramp.txt

# Topo line distance
T=10

# Topo resample
RESAMPLE=500

all: hillshade relief slope contour

webmercator:
	gdalwarp -s_srs $(SOURCE_PROJECTION) -t_srs EPSG:3785 -r bilinear -co compress=lzw $(INPUT).tif $(INPUT)_mercator.tif

hillshade: webmercator
	gdaldem hillshade -co compress=lzw -az $(AZIMUTH) -alt $(ALTITUDE) -z $(EXAGERATE) $(INPUT)_mercator.tif $(INPUT)_hillshade.tif

relief: webmercator
	gdaldem color-relief $(INPUT)_mercator.tif $(RAMP) $(INPUT)_relief.tif

slope: webmercator
	gdaldem slope $(INPUT)_mercator.tif $(INPUT)_slope.tif
	gdaldem color-relief -co compress=lzw $(INPUT)_slope.tif slope-ramp.txt $(INPUT)_slope_ramp.tif

contour: webmercator
	gdal_contour -a ELEV -i $T $(INPUT)_mercator.tif $(INPUT)_elevation.shp


clean:
	rm -f *_mercator.tif *_hillshade.tif *_relief.tif *_ramp.tif *_slope_ramp.tif *_slope.tif *.shp *.dbf *.prj *.shx

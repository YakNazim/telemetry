# Original Filenames
INPUT = SRTM_Brothers

# STRM geotiff come in WGS84
SOURCE_PROJECTION=EPSG:4326

# Hillshade options
AZIMUTH=330
ALTITUDE=60

# Color relief options
RAMP=colorramp.txt

all: hillshade relief slope

webmercator:
	gdalwarp -s_srs $(SOURCE_PROJECTION) -t_srs EPSG:3785 -r bilinear -co compress=lzw $(INPUT).tif $(INPUT)_mercator.tif

hillshade: webmercator
	gdaldem hillshade -co compress=lzw -az $(AZIMUTH) -alt $(ALTITUDE) $(INPUT)_mercator.tif $(INPUT)_hillshade.tif

relief: webmercator
	gdaldem color-relief $(INPUT)_mercator.tif $(RAMP) $(INPUT)_relief.tif

slope: webmercator
	gdaldem slope $(INPUT)_mercator.tif $(INPUT)_slope.tif
	gdaldem color-relief -co compress=lzw $(INPUT)_slope.tif slope-ramp.txt $(INPUT)_slope_ramp.tif

clean:
	rm -f *_mercator.tif *_hillshade.tif *_relief.tif *_ramp.tif *_slope_ramp.tif *_slope.tif

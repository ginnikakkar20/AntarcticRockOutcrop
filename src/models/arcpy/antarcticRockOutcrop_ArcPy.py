#! /usr/bin/env python
###############################################################################
# Rock Outcrop Identification using Landsat-8 tiles
#
# --- Description ---
# This script applies the method of Burton-Johnson, et al. [1] to automatically
# identify rock outcrop areas from top of atmosphere corrected Landsat-8 
# tiles from Antarctica. Relevant modifications should be made for application
# to other Landsat datasets where band numbers may change.
#
# --- Requirements ---
# ArcGIS >9.0
# Spatial Analyst Extension
#
# --- Usage ---
# Please set the appropriate input and output directories on Lines 38-44 of
# this script prior to running. Top of atmosphere corrected Landsat-8 
# tiles can be downloaded from USGS ESPA at https://espa.cr.usgs.gov.
#
# The first step in submitting an order for ESPA is to create a scene list.
# This is a simple text file (*.txt) listing one Landsat identifier (filename)
# on each line. The list can be easily generated by performing a spatial/temporal 
# inventory search through EarthExplorer (http://earthexplorer.usgs.gov/) and
# exporting search results to a spreadsheet from which filenames can be extracted.
#
# Once ESPA tiles are downloaded *ALL* tiles should be extract to the *SAME* root
# directory for processing with this script. The text file of Landsat IDs 
# required by ESPA is the same as required by this script.
#
# The coastline mask can either be created manually or the current Antarctic
# coastline can be downloaded as a shapefile from the Antarctic Digital
# Database: http://www.add.scar.org
#
# This script should be run either within ArcMap from the Python console 
# (Geoprocessing > Python), or from the ArcMap python command line launched 
# from Start > Programs > ArcGIS > Python X.X > Python (command line).
# Once in Python, simply "execfile" using the full path to this script with 
# escaped slashes (double backslash: \\), as per the example below.
#
# To avoid any problems please ensure all files have the same geospatial
# referencing system.
#
# --- Inputs/Outputs ---
#	# Inputs:
#	<landsatTileList>, string
#		Exact path to Landsat tile list (*.txt).
#		One landsat Tile ID on each line.
#		Each tile should be in the <landsatDirectory>.
#	<landsatDirectory>, string
#		Exact path to directory of extracted ESPA tiles.
#		No trailing slash.
#		Tilenames should follow ESPA convections:
#			TILEID_toa_bandX.tif
#	<coastMaskShpfile>
#		Exact path to coastline shapefile (.shp).
#
#	# Outputs:
#	<outputDirectory>, string
#		Exact path to output directory.
# 		Directory should already exist.
#		No trailing slash.
#	<outputFileExt>, string
#		Suffix for output file names, e.g. "_rock.tif".
#		Should always start with underscore (_).
#		Should always end with ".tif".
#		Prefixed automatically with the Tile ID.
#
# --- Example ---
# #Launch an ArcPy console and run:
# execfile("C:\\path\\to\\script\\arcpy_outcrop_ID_landsat8.py")
#
# --- Reference ---
# [1] Burton-Johnson, A., Black, M., Fretwell, P. T., and Kaluza-Gilbert, J.: 
#		A fully automated methodology for differentiating rock from snow, clouds 
#		and sea in Antarctica from Landsat imagery: A new rock outcrop map and 
#		area estimation for the entire Antarctic continent, The Cryosphere 
#		Discuss., doi:10.5194/tc-2016-56, in review, 2016. 
#
# --- Author ---
# Author: Martin Black
# Email: martin.black@bas.ac.uk
# Date: 2015-03-11
# Version: 1.0
#
# --- License ---
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

#imports
import arcpy, sys, os, time
from arcpy import env  
from arcpy.sa import *  

#set arcpy environment variables
#arcpy.env.overwriteOutput = True #uncomment to allow arcpy to overwrite outputs

#inputs (tile list file, directory containing tiles, coastline for masking)
landsatTileList  = r"C:/path/to/landsatTilesToProcess.txt"
landsatDirectory = r"C:/path/to/folder/of/all/landsat/tiles"
coastMaskShpfile = r"C:/path/to/coastline.shp" 

#outputs (file extension, output directory)
outputDirectory = r"C:/path/to/outputs"
outputFileExt   = r"_fileSuffix.tif"

###############################################################################
#checkout ArcGIS spatial analyst extension license
arcpy.CheckOutExtension("Spatial")

#create tile ID list from an ESPA style text file
tiles = open(landsatTileList).read().splitlines()

#print the start time
startTime = time.ctime()
print "ArcPy Rock masking script started: %s" % startTime

#loop through each raster
for i in range(len(tiles)):

	#set up a couple of filename strings we'll need later
	thisTileID   = tiles[i]
	thisTileFile = landsatDirectory + "/" + thisTileID
	outFilename  = outputDirectory  + "/" + thisTileID

	#print the file we're doing
	fmt = "\t%d of %d."
	print( fmt % ( i+1, len(tiles) ) ),
	tic=time.time();	

	#grab the band data (LANDSAT-8 OLI, bands are stacked, no Panchromatic band)
	B2  = Raster(thisTileFile + "_toa_band2.tif")  #Blue
	B3  = Raster(thisTileFile + "_toa_band3.tif")  #Green
	B5  = Raster(thisTileFile + "_toa_band5.tif")  #NIR
	B6  = Raster(thisTileFile + "_toa_band6.tif")  #SWIR1
	B10 = Raster(thisTileFile + "_toa_band10.tif") #TIRS1

	#float each raster
	B2  = Float(B2)
	B3  = Float(B3)
	B5  = Float(B5)
	B6  = Float(B6)
	B10 = Float(B10)

	#extract by mask on coastline
	coastMask = ExtractByMask(B2, coastMaskShpfile)
	coastMaskBin = coastMask > 0

	#print the coast mask
	toc=time.time();
	print(" Loaded & Coast Masked (%.02fs)." % (toc-tic)),
	tic=time.time();		

	#ratios
	ndsi = (B3 - B6)/(B3 + B6)
	ndwi = (B3 - B5)/(B3 + B5)

	#mask 1, sunlit rock
	mask1_step1 = ( B10/B2 ) > 0.4
	mask1_step2 = ndsi < 0.75
	mask1_step3 = ndwi < 0.45
	mask1_step5 = B10 > 2550 #note this is a scaled value
	mask1_prefinal = Int(mask1_step1) + Int(mask1_step2) + Int(mask1_step3) + Int(coastMaskBin) + Int(mask1_step5)
	mask1_final    = mask1_prefinal == 5

	#mask 2, rock in shade
	mask2_step1 = B2 < 2500 #note this is a scaled value
	mask2_step2 = ndwi < 0.45
	mask2_prefinal = Int(mask2_step1) +  Int(mask2_step2) + Int(coastMaskBin)
	mask2_final    = mask2_prefinal == 3

	#combine mask1 and mask2
	mask_prefinal = mask1_final + mask2_final;
	mask_final    = mask_prefinal > 0

	#print the processing time
	toc=time.time();
	print(" Processed (%.02fs)." % (toc-tic)),	
	tic=time.time();

	#save output
	mask_final.save(outFilename + outputFileExt)

	#print the save time
	toc=time.time();
	print(" Saved (%.02fs)." % (toc-tic))	

#script closing output 
endTime = time.ctime()
print "ArcPy Rock masking script finished: %s" % endTime
###############################################################################

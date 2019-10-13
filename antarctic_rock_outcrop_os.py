#! /usr/bin/env python
"""
Rock Outcrop Identification using Landsat-8 tiles

--- Description ---
This script applies the method of Burton-Johnson, et al. [1] to automatically
identify rock outcrop areas from top of atmosphere corrected Landsat-8 
tiles from Antarctica. Relevant modifications should be made for application
to other Landsat datasets where band numbers may change.

--- Requirements ---
ArcGIS >9.0
Spatial Analyst Extension

--- Usage ---
Please set the appropriate input and output directories on Lines 38-44 of
this script prior to running. Top of atmosphere corrected Landsat-8 
tiles can be downloaded from USGS ESPA at https://espa.cr.usgs.gov.

The first step in submitting an order for ESPA is to create a scene list.
This is a simple text file (*.txt) listing one Landsat identifier (filename)
on each line. The list can be easily generated by performing a spatial/temporal 
inventory search through EarthExplorer (http://earthexplorer.usgs.gov/) and
exporting search results to a spreadsheet from which filenames can be extracted.

Once ESPA tiles are downloaded *ALL* tiles should be extract to the *SAME* root
directory for processing with this script. The text file of Landsat IDs 
required by ESPA is the same as required by this script.

The coastline mask can either be created manually or the current Antarctic
coastline can be downloaded as a shapefile from the Antarctic Digital
Database: http://www.add.scar.org

This script should be run either within ArcMap from the Python console 
(Geoprocessing > Python), or from the ArcMap python command line launched 
from Start > Programs > ArcGIS > Python X.X > Python (command line).
Once in Python, simply "execfile" using the full path to this script with 
escaped slashes (double backslash: \\), as per the example below.

To avoid any problems please ensure all files have the same geospatial
referencing system.

--- Inputs/Outputs ---
Inputs:
<landsatTileList>, string
	Exact path to Landsat tile list (*.txt).
	One landsat Tile ID on each line.
	Each tile should be in the <landsatDirectory>.
        <landsatDirectory>, string
	Exact path to directory of extracted ESPA tiles.
		No trailing slash.
		Tilenames should follow ESPA convections:
			TILEID_toa_bandX.tif
	<coastMaskShpfile>
		Exact path to coastline shapefile (.shp).

	# Outputs:
	<outputDirectory>, string
		Exact path to output directory.
 		Directory should already exist.
		No trailing slash.
	<outputFileExt>, string
		Suffix for output file names, e.g. "_rock.tif".
		Should always start with underscore (_).
		Should always end with ".tif".
		Prefixed automatically with the Tile ID.

 --- Example ---
 #Launch an ArcPy console and run:
execfile("C:\\path\\to\\script\\arcpy_outcrop_ID_landsat8.py")

--- Reference ---
[1] Burton-Johnson, A., Black, M., Fretwell, P. T., and Kaluza-Gilbert, J.: 
	A fully automated methodology for differentiating rock from snow, clouds 
		and sea in Antarctica from Landsat imagery: A new rock outcrop map and 
		area estimation for the entire Antarctic continent, The Cryosphere 
		Discuss., doi:10.5194/tc-2016-56, in review, 2016. 

 --- Author ---
Author: Martin Black
Email: martin.black@bas.ac.uk
Date: 2015-03-11
Version: 1.0

 --- Rewritten to remove ArcGIS and ArcPy requirement ---
 Refactorer: Sam Elkind
 Email: selkind3@gatech.edu
 Date: 2019-13-10
 Version: 0.1

--- License ---
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

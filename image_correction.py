"""
Class that corrects Landsat 8 OLI reflective bands to Top of Atmosphere Reflectance
and Thermal bands to Top of Atmosphere Brightness Temperature as defined
by https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level **ADD REST OF URL**

"""
import os


class LandsatTOACorrecter:

    # These values are specific to MTL.txt file provided by AWS (and maybe google too?)
    self.K1_PREFIX = "K1_CONSTANT_BAND_"
    self.K2_PREFIX = "K2_CONSTANT_BAND_"
    self.REFLECTANCE_MULT_PREFIX = "REFLECTANCE_MULT_BAND_"
    self.REFLECTANCE_ADD_PREFIX = "REFLECTANCE_ADD_BAND_"
    self.SUN_ELEV_PREFIX = "SUN_ELEVATION"


    """
    @param str scene_path: The absolute path to directory of a specific landsat scene containing
                            all bands.
    """


    def __init__(self, scene_path):
        self.path = scene_path
        self.scene_id = ""
        self.base_dir = ""
        self.mtl_path = ""
        self.configure_paths()

        # convert dict to named tuple eventually
        self.refl_vars = {}
        self.K1 = {"K1_CONSTANT_BAND": None, "K1_CONSTANT_BAND_11": None,}
                
        self.K2 = {}

    def configure_paths(self):
        assert os.path.exists(self.path)
        assert os.path.isdir(self.path)
        self.scene_id = os.path.basename(self.path)
        self.base_dir = os.path.dirname(self.path)
        self.mtl_path = self.base_dir + "/" + self.scene_id + "/" + self.scene_id + "_MTL.txt"
        assert os.path.exists(self.mtl_path)

    def gather_correction_vars(self):

        with 



if __name__ == "__main__":
    test_img_path = "/home/dsa/DSA/images/LC82201072015017LGN00"

    test = LandsatTOACorrecter(test_img_path)


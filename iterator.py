"""Iterator class for training data"""

import parsing

from os import listdir
from os.path import isfile, join


class Iterator(object):
    def __init__(self, contour_dir, dcm_dir):
        self.contour_dir = contour_dir
        self.dcm_dir = dcm_dir
        self.position = 0
        self.contour_list = [f for f in listdir(self.contour_dir) if isfile(join(contour_path, f)) and
                         f.endswith('.txt') and f.startswith('IM')]


    def __iter__(self):
        return self

    def next(self):
        """
               Returns the next training tuple (256x256 DICOM Image array, Bit Mask)
        """

        check = False

        # Go through contours until we get a valid contour and  corresponding DICOM Image
        while not check:
            if self.position >= len(self.contour_list):
                raise StopIteration

            contour_file = self.contour_dir + self.contourlist[self.position]
            coords_list = parsing.parse_contour_file(contour_file)

            # If coordinates are empty continue
            if coords_list is None:
                self.position += 1
                continue
            dcm_file = parsing.contour_to_dicome_filename(contour_file, self.dcm_dir)

            # If not a valid file continue
            if not isfile(dcm_file):
                self.position += 1
                continue
            else:
                dcm_dict = parsing.parse_dicom_file(dcm_file)
                if dcm_dict == None:
                    self.position += 1
                    continue
                else:
                    try:
                        width, height = dcm_dict['pixel_data'].shape
                    except KeyError:
                        self.position += 1
                        continue
                    mask = parsing.poly_to_mask(coords_list, width, height)
                    check = True
        return mask



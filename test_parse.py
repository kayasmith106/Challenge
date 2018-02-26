"""Source code for some tests"""
import plot
import parsing
from os import listdir
from os.path import isfile, join

def create_border_plots(data_dir,link_dict):

    for pat_id, orig_id in zip(link_dict['patient_id'], link_dict['original_id']):

        dcm_path = data_dir + 'dicoms/' + pat_id + '/'
        contour_path = data_dir + 'contourfiles/' + orig_id + '/i-contours/'

        contour_files = [f for f in listdir(contour_path) if isfile(join(contour_path, f)) and f.endswith('.txt') and f.startswith('IM')]

        for contour in contour_files:
            coords_list = parsing.parse_contour_file(contour_path + contour)
            if coords_list is None:
                continue
            else:
                dcm_file = dcm_path + contour[8:12].lstrip('0') + '.dcm'
                if isfile(dcm_file):
                    dcm_dict = parsing.parse_dicom_file(dcm_file)
                    if dcm_dict is None:
                        continue
                    else:
                        try:
                            width, height = dcm_dict['pixel_data'].shape
                        except KeyError:
                            continue
                        mask = parsing.poly_to_mask(coords_list, width, height)
                        outfile = 'plots/borderplot_' + contour[8:12].lstrip('0') + '.jpg'
                        print("------ Plotting ------", outfile)
                        plot.plot_polygon_with_mask(coords_list, mask, outfile)


if __name__ == "__main__":

    print("------ Testing the polygon drawing ------")
    data_path = "C:/Users/k.smith/Desktop/Coding Challenge/final_data/final_data/"
    link_dict = parsing.parse_link_csv(data_path)
    create_border_plots(data_path, link_dict)



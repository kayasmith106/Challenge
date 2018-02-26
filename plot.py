"""Plotting code for looking at polygons vs  mask"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_polygon_with_mask(points, mask, out_file):
    """
    Plot the border of the mask on a plot of the slice and mask
    the plot is not shown but saved to a file


    :param points: a list of (x,y) points indicating the vertices of the polygone
    :param mask: mask array (2D), should have the same shape as slice
    :param outfile: filepath to which the plot will be saved to
    """

    f = plt.figure(figsize=(125, 125))
    f.add_subplot(1, 1, 1)
    plt.imshow(mask, cmap=plt.cm.bone)
    plt.scatter(*zip(*points), s=5)
    f.savefig(out_file, bbox_inches='tight')
    plt.close('all')
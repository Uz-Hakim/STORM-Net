from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np
import cv2



image_hsv = None
pixel = (0, 0, 0) #RANDOM DEFAULT VALUE
ftypes = [
    ('JPG', '*.jpg;*.JPG;*.JPEG'),
    ('PNG', '*.png;*.PNG'),
    ('GIF', '*.gif;*.GIF'),
]


def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(lower, upper)

        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
        image_mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow("Mask", image_mask)


class Arrow3D(FancyArrowPatch):
    """
    draws a 3D arrow onto a renderer
    """
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def plot_3d_pc(ax, data, selected, names=None):
    """
    plots a 3d point cloud representation of data
    :param ax: the axis to plot into
    :param data: the data (nx3 numpy array)
    :param selected: an int representing the currently selected data point - will be painted red
    :param names: the names of the data points
    :return:
    """
    if not names:
        names = [str(i) for i in range(len(data))]
    colors = ['b'] * len(data)
    colors[selected] = 'r'
    data_min = np.min(data, axis=0)
    a = Arrow3D([data_min[0], data_min[0]+3], [data_min[1], data_min[1]],
                [data_min[2], data_min[2]], mutation_scale=10,
                lw=1, arrowstyle="-|>", color="r")
    b = Arrow3D([data_min[0], data_min[0]], [data_min[1], data_min[1]+3],
                [data_min[2], data_min[2]], mutation_scale=10,
                lw=1, arrowstyle="-|>", color="r")
    c = Arrow3D([data_min[0], data_min[0]], [data_min[1], data_min[1]],
                [data_min[2], data_min[2]+3], mutation_scale=10,
                lw=1, arrowstyle="-|>", color="r")
    if selected < len(data) -1:
        d = Arrow3D([data[selected, 0], data[selected+1, 0]], [data[selected, 1], data[selected+1, 1]],
                    [data[selected, 2], data[selected+1, 2]], mutation_scale=10,
                    lw=1, arrowstyle="-|>", color="r")
        ax.add_artist(d)
    ax.add_artist(a)
    ax.add_artist(b)
    ax.add_artist(c)
    for i, (c, x, y, z) in enumerate(zip(colors, data[:, 0], data[:, 1], data[:, 2])):
        ax.scatter(x, y, z, marker='o', c=c)
        ax.text(x + 0.2, y + 0.2, z + 0.2, '%s' % (names[i]), size=6, zorder=1, color='k')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_title('Point {} (WASD: change view, Arrows: next/previous point)'.format(selected))

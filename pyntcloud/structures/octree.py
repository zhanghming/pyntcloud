#  HAKUNA MATATA

"""
VoxelGrid Class
"""

import numpy as np
import pandas as pd


class Octree(object):
    
    def __init__(self, points, max_level=2):
        self.points = points
        self.max_level= max_level
        self.structure = np.zeros((self.points.shape[0], self.max_level*3), dtype=bool)
        xyzmin = points.min(0)
        xyzmax = points.max(0)
        #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
        diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
        xyzmin = xyzmin - diff / 2
        xyzmax = xyzmax + diff / 2
        self.xyzmin = xyzmin
        self.xyzmax = xyzmax
        self.id = "O({})".format(max_level)
        self.build()

    def build(self):
        self.sizes = np.zeros(self.max_level)
        level_ptp = max(self.xyzmax-self.xyzmin) / 2
        mid_points = np.zeros_like(self.points)
        mid_points[:] = (self.xyzmin + self.xyzmax) / 2
        n = 0
        for i in range(self.max_level):
            self.sizes[i] = level_ptp
            level_ptp /= 2
            bigger = self.points > mid_points
            self.structure[:, n:n+3] = bigger
            if i != self.max_level - 1:
                mid_points = np.where(bigger, mid_points + level_ptp, mid_points - level_ptp)
                n += 3

    def get_level_as_sf(self, level):
        sf = np.arange(len(self.points))
        st = pd.DataFrame(np.packbits(self.structure[:,:level*3], axis=1))
        i = 0
        for g in st.groupby([x for x in  st.columns]).apply(lambda x: x.index.values).values:
            sf[g] = i
            i+=1

        return sf




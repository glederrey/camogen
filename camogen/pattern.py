#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)

import numpy as np
from random import shuffle


class Pattern:
    """
    The pattern is composed of sets of Polygons
    """

    def __init__(self, parameters):
        """
        Pass the parameters in JSON to the Pattern to initialize it

        :param parameters: JSON of the parameters
        """

        try:
            # General parameters
            self.width = np.abs(parameters['width'])
            self.height = np.abs(parameters['height'])
            self.polygon_size = max(150, np.abs(parameters['polygon_size']))
            self.color_bleed = np.abs(parameters['color_bleed'])
            if 'max_depth' in parameters.keys():
                self.max_depth = min(15, np.abs(parameters['max_depth']))
            else:
                self.max_depth = 15
            self.colors = parameters['colors']

            # Spots
            if 'spots' in parameters.keys():
                self.spots_nbr = min(20000, np.abs(parameters['spots']['amount']))
                self.spots_radius_min = max(5, min(100, np.abs(parameters['spots']['radius']['min'])))
                self.spots_radius_max = max(5, min(100, np.abs(parameters['spots']['radius']['max'])))
                self.spots_sampling = np.abs(parameters['spots']['sampling_variation'])
            else:
                self.spots_nbr = 0

            # Pixelize
            if 'pixelize' in parameters.keys():
                self.pixelize_percentage = min(1, np.abs(parameters['pixelize']['percentage']))
                self.pixelize_sampling = np.abs(parameters['pixelize']['sampling_variation'])
                self.pixelize_density_x = max(10, np.abs(parameters['pixelize']['density']['x']))
                self.pixelize_density_y = max(10, np.abs(parameters['pixelize']['density']['y']))
            else:
                self.pixelize_percentage = 0

            # List of Polygons
            self.list_polygons = []
            self.nbr_polygons = 0

        except KeyError:
            raise KeyError("Please check that your parameter dictionary is correctly written.")

    def add_polygon(self, p):
        """
        Add a polygon to the list of polygon

        :param p: Polygon
        """
        if type(p).__name__ != 'Polygon':
            raise ValueError("Element should be of the class Polygon")

        self.list_polygons.append(p)

    def suffle_polygons(self):
        """
        Shuffle and count the number of polygons

        Shuffling is done such that the color does not depend on the order of the polygons
        """

        self.nbr_polygons = len(self.list_polygons)

        shuffle(self.list_polygons)
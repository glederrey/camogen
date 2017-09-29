#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Astrom (http://www.happyponyland.net)

from camogen.helpers import *


class Polygon:
    """
    Set of vertices defining a surface
    (Last vertex connects to first)
    """

    def __init__(self, color_index=None):
        """
        Constructor with the color index
        :param color_index: Index of the color
        """
        self.color_index = color_index
        self.list_vertices = []
        self.list_neighbours = []

    def circumference(self):
        """
        Compute the circumference of the polygon
        (Sums the distance between all vertices)

        :return: value for the circumference
        """
        total = 0

        # Number of vertices
        nbr_vertices = len(self.list_vertices)

        for i in range(nbr_vertices):
            va = self.list_vertices[i]
            vb = self.list_vertices[(i+1) % nbr_vertices]

            total += dist_vertices(va, vb)

        return total

    def add_vertex(self, v):
        """
        Add a vertex to the list of vertices

        :param v: Vertex
        """
        if type(v).__name__ != 'Vertex':
            raise ValueError("Element should be of the class Vertex")

        self.list_vertices.append(v)

    def add_vertices(self, vs):
        """
        Add a list of vertices to the list of vertices

        :param vs: List of vertices
        """

        for v in vs:
            if type(v).__name__ != 'Vertex':
                raise ValueError("Element should be of the class Vertex")

        self.list_vertices.extend(vs)

    def add_neighbour(self, idx):
        """
        Add a neighbour to the list of neighbours

        :param p: Index of a polygon
        """

        self.list_neighbours.append(idx)

    def to_string(self):
        """
        Print the Polygon. For debug purpose

        :return: String of the polygon
        """
        return "Polygon: {" + ", ".join([v.to_string() for v in self.list_vertices]) + "}"

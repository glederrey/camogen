#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Astrom (http://www.happyponyland.net)


class Vertex:
    """
    Defines a point on the canvas
    """
    def __init__(self, x, y):
        """
        Constructor for the vertex

        :param x: horizontal coordinate
        :param y: vertical coordinate
        """
        self.x = x
        self.y = y

    def to_string(self):
        """
        Print the Vertex. For debug purpose

        :return: String of the vertex
        """
        return "Vertex ({:.2f}, {:.2f})".format(self.x, self.y)




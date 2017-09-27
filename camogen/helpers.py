#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)


from camogen.vertex import *
import numpy as np


def distort():
    """
    :return: random value between 0 and 1
    """
    # return np.random.rand()
    return np.random.randint(10)/11


def dist_vertices(v1, v2):
    """
    Distance between two vertices

    :param v1: Vertex
    :param v2: Vertex
    :return: distance
    """

    if type(v1).__name__ != 'Vertex':
        raise ValueError("Element v1 should be of the class Vertex")

    if type(v2).__name__ != 'Vertex':
        raise ValueError("Element v2 should be of the class Vertex")

    return np.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)


def edge_split(v1, v2, frac):
    """
    Split the edge between v1 and v2. frac is the fraction of length between the new edge and v1.

    :param v1: Vertex 1
    :param v2: Vertex 2
    :param frac: fraction
    :return: new Vertex
    """

    if type(v1).__name__ != 'Vertex':
        raise ValueError("Element v1 should be of the class Vertex")

    if type(v2).__name__ != 'Vertex':
        raise ValueError("Element v2 should be of the class Vertex")

    if frac >= 1 or frac <= 0:
        raise ValueError("Fraction is between 0 and 1 non-included")

    if v1.x < v2.x:
        new_x = v1.x + np.abs(v2.x - v1.x) * frac
    else:
        new_x = v1.x - np.abs(v2.x - v1.x) * frac

    if v1.y < v2.y:
        new_y = v1.y + np.abs(v2.y - v1.y) * frac
    else:
        new_y = v1.y - np.abs(v2.y - v1.y) * frac

    return Vertex(new_x, new_y)


def new_edge(va1, va2, vb1, vb2):
    """
    Create a new edge between edge A and edge B.

    Edge A is represented by two vertices va1 and va2.
    Edge B is represented by two vertices vb1 and vb2.

    :param va1: Vertex
    :param va2: Vertex
    :param vb1: Vertex
    :param vb2: Vertex
    :return: list[Vertex]
    """

    if type(va1).__name__ != 'Vertex':
        raise ValueError("Element va1 should be of the class Vertex")

    if type(va2).__name__ != 'Vertex':
        raise ValueError("Element va2 should be of the class Vertex")

    if type(vb1).__name__ != 'Vertex':
        raise ValueError("Element vb1 should be of the class Vertex")

    if type(vb2).__name__ != 'Vertex':
        raise ValueError("Element vb2 should be of the class Vertex")

    # Compute the fractions
    frac_a = 0.4 + np.random.randint(3)/10
    frac_b = 0.4 + np.random.randint(3)/10

    # Split Edge A
    new_vert_a = edge_split(va1, va2, frac_a)

    # Split Edge B
    new_vert_b = edge_split(vb1, vb2, frac_b)

    return [new_vert_a, new_vert_b]


def draw_polygons(draw, pattern, use_index):
    """
    Draw the polygons. Colors is either computed using the index of the polygons or their true color.

    :param image_draw: ImageDraw from PIL
    :param pattern: Pattern
    :param use_index: Boolean for the color
    :return: ImageDraw updated
    """

    for i, polygon in enumerate(pattern.list_polygons):

        color = pattern.colors[polygon.color_index] if not use_index else "#%06x" % i

        polygon_thick(draw, [(v.x, v.y) for v in polygon.list_vertices], color)


def polygon_thick(draw, points, color):
    draw.line(points, fill=color, width=2)
    draw.polygon(points, fill=color)


def find_neighbours(image, pattern):
    """
    Find the neighbours for all the polygons in the pattern

    :param image: Image from PIL
    :param pattern: Pattern
    """

    # We check every corner of every polygon with a sample point just a few pixels outside. The color found
    # there will be the index of the polygon there, and the two polygons will be marked as neighbours.
    for i, polygon in enumerate(pattern.list_polygons):
        nbr_edges = len(polygon.list_vertices)

        # Go through all edges
        for e in range(nbr_edges):

            # We need to compare the (c)urrent corner to the (n)ext and (p)revious.
            # For example, if the previous corner is to the right and the next is below, it should be pointing northwest
            # This is the direction we will place our sample point

            c = polygon.list_vertices[e]
            n = polygon.list_vertices[(e + 1) % nbr_edges]
            p = polygon.list_vertices[(e - 1) % nbr_edges]

            # Offsets
            x_off = 0
            y_off = 0

            # NE, NW, SW, SE
            if n.x < c.x:
                x_off += 1
            if p.y > c.y:
                y_off -= 1

            if p.x > c.x:
                x_off -= 1
            if n.y > c.y:
                y_off -= 1

            if n.x > c.x:
                x_off -= 1
            if p.y < c.y:
                y_off += 1

            if p.x < c.x:
                x_off += 1
            if n.y < c.y:
                y_off += 1

            # Coordinate of the point to test
            x = c.x + x_off
            y = c.y + y_off

            # We check that the point is in the image
            if 0 <= x < pattern.width and 0 <= y < pattern.height:

                # Get its color and transform it into hex
                r, g, b = image.getpixel((x, y))
                hex = '#%02x%02x%02x' % (r, g, b)

                # Transform the hex value into the index
                idx = int(hex[1:], 16)

                # And if it's a valid point, we add the neighbours
                if idx < len(pattern.list_polygons) and idx != i:
                    polygon.add_neighbour(idx)
                    pattern.list_polygons[idx].add_neighbour(i)

    # It's possible that there are some duplicates, so remove them
    for polygon in pattern.list_polygons:
        polygon.list_neighbours = list(set(polygon.list_neighbours))


def color_polygon(pattern, index, color, bleed):
    """
    Color the polygons recursively

    :param pattern: Pattern
    :param index: Starting index for the polygons
    :param color: Index of the color
    :param bleed: Value for the color bleed
    """

    polygon = pattern.list_polygons[index]
    polygon.color_index = color

    # Check if we have to go further in the recursion
    if bleed > 0:
        # We need to make a list of neighbours for this polygon that do not have a color yet. We sort these
        # according to who has the most neighbors of the same color - this will make polygons of the same color
        # more likely to stick together.

        candidates = []
        nbr_neighbors_same_color = []
        for neigh_index in polygon.list_neighbours:
            if pattern.list_polygons[neigh_index].color_index is None:
                candidates.append(neigh_index)
                nbr_neighbors_same_color.append(colored_neighbours(pattern, neigh_index, color))

        if len(candidates) > 0:
            idx_sorted = np.argsort(nbr_neighbors_same_color)[::-1]
            color_polygon(pattern, candidates[idx_sorted[0]], color, bleed - 1)


def colored_neighbours(pattern, index, color):
    """
    Count the number of neighbours with the color

    :param pattern: Pattern
    :param index: Index of a Polygon
    :param color: color
    :return: Int
    """

    polygon = pattern.list_polygons[index]

    count = 0

    for neigh_index in polygon.list_neighbours:
        other_polygon = pattern.list_polygons[index]

        if other_polygon.color_index == color:
            count += 1

    return count


def add_spots(pattern, image, draw):
    """
    Add the spots to the image

    :param pattern: Pattern
    :param image: Image from PIL
    :param draw: ImageDraw from PIL
    """

    spots_to_add = pattern.spots_nbr
    while spots_to_add:

        # Radius of the spot
        spot_radius = np.random.randint(pattern.spots_radius_min, pattern.spots_radius_max)/2

        # Position of the spot
        spot_x = np.random.randint(spot_radius, pattern.width-spot_radius)
        spot_y = np.random.randint(spot_radius, pattern.height-spot_radius)

        # Pick a sampling point slightly off the spot center. Make sure it's on the canvas
        sample_x = spot_x - pattern.spots_sampling + np.random.randint(pattern.spots_sampling*2 + 1)
        sample_x = min(pattern.width-1, max(0, sample_x))

        sample_y = spot_y - pattern.spots_sampling + np.random.randint(pattern.spots_sampling * 2 + 1)
        sample_y = min(pattern.width-1, max(0, sample_y))

        # Get the color at this spot
        r, g, b = image.getpixel((int(sample_x), int(sample_y)))
        hex = '#%02x%02x%02x' % (r, g, b)
        draw.ellipse((spot_x - spot_radius, spot_y - spot_radius, spot_x + spot_radius, spot_y + spot_radius), fill=hex)

        spots_to_add -= 1


def pixelize(pattern, image, draw):
    """
    Pixelize the image

    :param pattern: Pattern
    :param image: Image from PIL
    :param draw: ImageDraw from PIL
    """

    if pattern.pixelize_percentage > 0:

        # Compute the width and height of the pixels
        pixel_w = int(pattern.width / pattern.pixelize_density_x)
        pixel_h = int(pattern.height / pattern.pixelize_density_y)

        # We loop through each pixel.
        for x in range(int(pixel_w/2), pattern.width, pixel_w):
            for y in range(int(pixel_h / 2), pattern.width, pixel_h):

                # Check if we pixelize this pixel
                if pattern.pixelize_percentage > np.random.rand():

                    # Sample a color slightly off the pixel center and draw this as a filled rectangle
                    sample_x = x - pattern.pixelize_sampling + np.random.randint(pattern.pixelize_sampling * 2 + 1)
                    sample_x = min(pattern.width - 1, max(0, sample_x))

                    sample_y = y - pattern.pixelize_sampling + np.random.randint(pattern.pixelize_sampling * 2 + 1)
                    sample_y = min(pattern.width-1, max(0, sample_y))
                    r, g, b = image.getpixel((int(sample_x), int(sample_y)))
                    hex = '#%02x%02x%02x' % (r, g, b)

                    draw.rectangle((x - pixel_w/2, y - pixel_h/2, x + pixel_w/2, y + pixel_h/2), fill=hex)



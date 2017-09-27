#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)


from camogen.polygon import *
from camogen.pattern import *
from camogen.helpers import *

from PIL import Image, ImageDraw


def generate_polygons(pattern, polygon, depth):
    """
    Main generator function

    :param pattern: [Pattern] Pattern specification to use
    :param polygon: [Polygon] Area on which the pattern in drawn
    :param depth: [int] Depth of the recursion
    """

    if type(pattern).__name__ != 'Pattern':
        raise ValueError("Element pattern should be of the class Pattern")

    if type(polygon).__name__ != 'Polygon':
        raise ValueError("Element polygon should be of the class Polygon")

    # Check if the circumference of the Polygon is small enough. If it's the case, we stop the recursion
    # We also check if we did enough recursive call. If it's the case, we also stop the recursion
    if polygon.circumference() < pattern.polygon_size or depth <= 0:
        pattern.add_polygon(polygon)
        pass
    else:

        # If none of these two conditions is fulfilled, we continue the recursive call

        # Compute the number of edges for this Polygon
        nbr_edges = len(polygon.list_vertices)

        # Make a list of all the edges length
        edge_lengths = []

        for i in range(nbr_edges):
            edge_lengths.append(dist_vertices(polygon.list_vertices[i], polygon.list_vertices[(i+1) % nbr_edges]))

        # We sort the edges in function of their lengths. We are interested in the indices
        idx_edge_sorted = np.argsort(edge_lengths)[::-1]

        # Let's take the two biggest edges
        # WARNING: We need to have them in order for the polygon splitting to work properly.
        # Therefore, a is the edge with the smallest index
        idx_edge_a = min(idx_edge_sorted[0], idx_edge_sorted[1])
        idx_edge_b = max(idx_edge_sorted[0], idx_edge_sorted[1])

        # We need to get the vertices of these edges
        va1 = polygon.list_vertices[idx_edge_a]
        va2 = polygon.list_vertices[(idx_edge_a + 1) % nbr_edges]

        vb1 = polygon.list_vertices[idx_edge_b]
        vb2 = polygon.list_vertices[(idx_edge_b + 1) % nbr_edges]

        # We create the new Polygons
        polygon_a = Polygon()
        polygon_b = Polygon()

        # Now, we generate the edge that will separate the two edges A and B
        edge_c = new_edge(va1, va2, vb1, vb2)

        # Stitch together the two new polygones. Each of them consists of "half" of the old polygon.
        # The dividing edge is included in both

        # Polygon A
        for i in range(0, idx_edge_a+1):
            polygon_a.add_vertex(polygon.list_vertices[i])

        for v in edge_c:
            polygon_a.add_vertex(v)

        for i in range(idx_edge_b+1, nbr_edges):
            polygon_a.add_vertex(polygon.list_vertices[i])

        # Polygon B
        for i in range(idx_edge_a+1, idx_edge_b+1):
            polygon_b.add_vertex(polygon.list_vertices[i])

        for v in edge_c[::-1]:
            polygon_b.add_vertex(v)

        generate_polygons(pattern, polygon_b, depth - 1)
        generate_polygons(pattern, polygon_a, depth - 1)


def generate_image(pattern):
    """
    Generate the final image
    :param pattern: Pattern with all the polygons
    :return: Image
    """

    image = Image.new('RGB', (pattern.width, pattern.height))

    draw = ImageDraw.Draw(image)

    # Draw each Polygon with its index as a color (this results in a lot of dark blue shades). We will use these
    # shades to detect which polygons border each other.
    draw_polygons(draw, pattern, use_index=True)

    # Now, we check the neighbours
    find_neighbours(image, pattern)

    # Make sure that the polygons do not have any colors
    for p in pattern.list_polygons:
        p.color_index = None

    # Now, we color them correctly
    # To do so, we go through every polygon and fill those that don't have any color.
    # Color bleed will usually fill more than one polygon (recursively), so the further we get through the loop,
    # the less likely we are to find colorless polygons.
    for i, polygon in enumerate(pattern.list_polygons):

        if polygon.color_index is None:
            color_polygon(pattern, i, np.random.randint(len(pattern.colors)), pattern.color_bleed)

    # Background
    draw.rectangle((0, 0, pattern.width-1, pattern.height-1), fill=pattern.colors[0])

    # Draw the polygons with their correct color
    draw_polygons(draw, pattern, use_index=False)

    # Now, we can do the postprocessing

    # We add the spots
    add_spots(pattern, image, draw)

    # We pixelize
    pixelize(pattern, image, draw)

    return image


def generate(parameters):
    """
    Generate the Camouflage pattern given the parameters

    :param parameters: Dictionnary of parameters
    :return: Image with the camouflage pattern
    """

    pattern = Pattern(parameters)
    starting_polygon = Polygon()

    first_vertices = [Vertex(pattern.width, 0),
                      # Vertex(pattern.width*distort(), 0),
                      Vertex(0, 0),
                      # Vertex(0, pattern.height*distort()),
                      Vertex(0, pattern.height),
                      # Vertex(pattern.width*distort(), pattern.height),
                      Vertex(pattern.width, pattern.height),
                      # Vertex(pattern.width*distort(), pattern.height*distort())
                      ]

    starting_polygon.add_vertices(first_vertices)

    # Generate a rough sketch of the pattern
    generate_polygons(pattern, starting_polygon, pattern.max_depth)

    # Shuffle the polygons
    pattern.suffle_polygons()

    # Generate the image
    image = generate_image(pattern)

    return image

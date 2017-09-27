#! /usr/bin/env python
# coding=utf-8
#
# Copyright © 2017 Gael Lederrey <gael.lederrey@epfl.ch>
#
# Distributed under terms of the MIT license.
#
# Based on the code of Ulf Alstrom (http://www.happyponyland.net/camogen.php)

import camogen

# Generate the examples given

# Green Blots
parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 6,
              'colors': ['#264722', '#023600', '#181F16'],
             'spots': {'amount': 20000, 'radius': {'min': 7, 'max': 14}, 'sampling_variation': 10}}

image = camogen.generate(parameters)
image.save('./images/green_blots.png')

# Mighty Swede
parameters = {'width': 700, 'height': 700, 'polygon_size': 400, 'color_bleed': 0,
              'colors': ['#668F46', '#4A6B3A', '#145000', '#003022']}

image = camogen.generate(parameters)
image.save('./images/mighty_swede.png')

# Vodka
parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 0,
              'colors': ['#2A4029', '#CCDED0', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF'],
             'spots': {'amount': 3000, 'radius': {'min': 30, 'max': 40}, 'sampling_variation': 10},
             'pixelize': {'percentage': 0.75, 'sampling_variation': 10, 'density': {'x': 60, 'y': 100}}}

image = camogen.generate(parameters)
image.save('./images/vodka.png')

# Maple Warrior
parameters = {'width': 700, 'height': 700, 'polygon_size': 150, 'color_bleed': 3,
              'colors': ['#072900', '#34611D', '#0C3000', '#7A6231', '#034700', '#092E00', '#00450E', '#043D00'],
             'spots': {'amount': 500, 'radius': {'min': 20, 'max': 30}, 'sampling_variation': 20},
             'pixelize': {'percentage': 1, 'sampling_variation': 20, 'density': {'x': 70, 'y': 50}}}

image = camogen.generate(parameters)
image.save('./images/maple_warrior.png')

# Desert
parameters = {'width': 700, 'height': 700, 'polygon_size': 400, 'color_bleed': 0,
              'colors': ['#B5A083', '#F7D6B4', '#F5CFA4', '#FAD7BB', '#EBD3A2', '#FCD5B3'],
             'spots': {'amount': 2500, 'radius': {'min': 8, 'max': 16}, 'sampling_variation': 14}}
image = camogen.generate(parameters)
image.save('./images/desert.png')

# Desert 2
parameters = {'width': 700, 'height': 700, 'polygon_size': 500, 'color_bleed': 0,
              'colors': ['#997948', '#C9AC31', '#FFE680'],
             'spots': {'amount': 2500, 'radius': {'min': 8, 'max': 16}, 'sampling_variation': 18}}
image = camogen.generate(parameters)
image.save('./images/desert2.png')

# Klosterschwester
parameters = {'width': 700, 'height': 700, 'polygon_size': 300, 'color_bleed': 3,
              'colors': ['#F0DFBD', '#9E704D', '#145000']}

image = camogen.generate(parameters)
image.save('./images/klosterschwester.png')
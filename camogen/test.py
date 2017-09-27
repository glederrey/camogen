import camogen

parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 6, 'max_depth': 15,
              'colors': ['#264722', '#023600', '#181F16'],
             'spots': {'amount': 20000, 'radius': {'min': 7, 'max': 14}, 'sampling_variation': 10},
             'pixelize': {'percentage': 0.1, 'sampling_variation': 20, 'density': {'x': 100, 'y': 100}}}

camogen.generate(parameters)
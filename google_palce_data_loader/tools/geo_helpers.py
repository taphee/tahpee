import geopy
from geopy import distance
import numpy as np
import pandas as pd


def build_circles_for_rectangle(west_south_point, east_north_point, box_width):
    w_s = (west_south_point['latitude'], west_south_point['longitude'])
    w_n = (west_south_point['latitude'], east_north_point['longitude'])
    e_s = (east_north_point['latitude'], west_south_point['longitude'])

    longitude_box_cnt = int(np.ceil(distance.vincenty(w_s, w_n).km / box_width))
    latitude_box_cnt = int(np.ceil(distance.vincenty(w_s, e_s).km / box_width))

    latitude_increment = abs((w_s[0] - e_s[0]) / latitude_box_cnt)
    longitude_increment = abs((w_n[1] - w_s[1]) / longitude_box_cnt)

    res = []
    for i in range(latitude_box_cnt):
        for j in range(longitude_box_cnt):
            box = {'west_south_point': (w_s[0] + latitude_increment * i, w_s[1] + longitude_increment * j),
                   'east_north_point': (w_s[0] + latitude_increment * (i + 1), w_s[1] + longitude_increment * (j + 1))}
            raw = {
                'circle_latitude': (box['west_south_point'][0] + box['east_north_point'][0]) / 2,
                'circle_longitude': (box['west_south_point'][1] + box['east_north_point'][1]) / 2,
                'radius': box_width / np.sqrt(2.75)
            }
            res.append(raw)

    return res


def get_bounding_box_of_circle(center_lon, center_lat, radious):
    start = geopy.Point(latitude=center_lat, longitude=center_lon)
    d = distance.VincentyDistance(kilometers=radious)

    # bearing=0 -> north
    # bearing=90 -> east
    # bearing=180 -> south
    # bearing=270 -> west
    east_north_point = {
        'longitude': d.destination(point=start, bearing=90).longitude,
        'latitude': d.destination(point=start, bearing=0).latitude
    }

    west_south_point = {
        'longitude': d.destination(point=start, bearing=270).longitude,
        'latitude': d.destination(point=start, bearing=180).latitude
    }

    return west_south_point, east_north_point


if __name__ == '__main__':
    # w_s, e_n = get_bounding_box_of_circle(-0.6882255844444194, 51.81401570927995, 1.414213562373095)
    import numpy as np
    import json
    import geog
    import shapely.geometry

    # 1.69705
    # 0.844992603
    RR = 1.05528
    w_s, e_n = get_bounding_box_of_circle(-0.096696, 51.532305, RR)

    p = shapely.geometry.Point([-0.096696, 51.532305])

    n_points = 20
    d = RR * 1000  # meters
    angles = np.linspace(0, 360, n_points)
    polygon = geog.propagate(p, angles, d)
    print(json.dumps(shapely.geometry.mapping(shapely.geometry.Polygon(polygon))['coordinates']) + ',')
    # print('========')
    circles = build_circles_for_rectangle(w_s, e_n, RR / 2)
    for x in circles:
        print(x)
        p = shapely.geometry.Point([x['circle_longitude'], x['circle_latitude']])
        n_points = 20
        d = x['radius'] * 1000  # meters
        angles = np.linspace(0, 360, n_points)
        polygon = geog.propagate(p, angles, d)
        print(json.dumps(shapely.geometry.mapping(shapely.geometry.Polygon(polygon))['coordinates']) + ',')

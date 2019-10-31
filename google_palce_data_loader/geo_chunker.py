from geopy import distance
import numpy as np
import pandas as pd


def build_area_circles(west_south_point, east_north_point, box_width):
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
                'radius': box_width / np.sqrt(2)
            }
            res.append(raw)

    return res


if __name__ == '__main__':
    # Kyiv
    w_s_lat = 50.21324216
    w_s_lon = 30.23639106
    e_n_lat = 50.59083299
    e_n_lon = 30.82765487

    box_width_km = 5

    result = build_area_circles(west_south_point={'latitude': w_s_lat,
                                                  'longitude': w_s_lon},

                                east_north_point={'latitude': e_n_lat,
                                                  'longitude': e_n_lon},
                                box_width=box_width_km)
    df = pd.DataFrame(result)
    df.to_csv(f'data/kyiv_{box_width_km}km.csv',
              sep=',',
              index=False)

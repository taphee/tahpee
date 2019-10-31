import os
import requests
import time
import random
import logging
from tqdm import tqdm
import csv
import pandas as pd

from googleplaces import GooglePlaces
from google_palce_data_loader.tools.geo_helpers import build_circles_for_rectangle, get_bounding_box_of_circle

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

GP_API_KEY = 'secret'
google_places = GooglePlaces(GP_API_KEY)


# '50.44399211166667,30.46632698611111,3.5355339059327373'

def geometry_to_lat_lng(item):
    item['lat'] = float(item.get('geometry').get('location').get('lat'))
    item['lng'] = float(item.get('geometry').get('location').get('lng'))
    item.pop('geometry', None)
    return item


def search_and_save_to_csv(lat, lng, radius, types, outpufile=None, next_page_token=None, cnt=0):
    time.sleep(random.uniform(1.15, 1.45))
    try:
        response = google_places.nearby_search(
            lat_lng={'lat': lat,
                     'lng': lng},
            radius=radius,
            types=types,
            pagetoken=next_page_token
        )
    except:
        with open('../data/problematic_circles.csv', 'a') as f:
            f.write(f'{lat},{lng},{radius / 1000}\n')
        logger.warning('\nRequest error for lat:{}, lng:{}'.format(lat, lng))
        return None

    response = response.raw_response
    results = [geometry_to_lat_lng(x) for x in response.get('results')]

    # when results more then 60 split circle into smaller circles and research
    cnt += len(results)
    if cnt >= 60:
        logger.info(f'\nFor circle {lng}, {lat} more then 60 results in radius - {radius}')
        w_s, e_n = get_bounding_box_of_circle(lng, lat, radius / 1000)
        for c in build_circles_for_rectangle(w_s, e_n, radius / 2000):
            search_and_save_to_csv(c['circle_latitude'],
                                   c['circle_longitude'],
                                   c['radius'] * 1000,
                                   type,
                                   outpufile=outpufile, cnt=0)

    fieldnames = ['lat', 'lng', 'icon', 'id', 'name', 'opening_hours',
                  'photos', 'place_id', 'plus_code', 'price_level', 'rating',
                  'reference', 'scope', 'types', 'user_ratings_total', 'vicinity']

    with open(f'data/{outpufile}.csv', 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if os.stat(f.name).st_size == 0:
            writer.writeheader()
        writer.writerows(results)

    if response.get('next_page_token'):
        time.sleep(random.uniform(1.65, 1.85))
        search_and_save_to_csv(lat, lng, radius, type, outpufile=outpufile,
                               next_page_token=response.get('next_page_token'), cnt=cnt)


if __name__ == '__main__':
    for lat, lng, radius in (50.447514, 30.494205, 3.54):
        search_and_save_to_csv(lat=lat,
                               lng=lng,
                               radius=radius * 1000,
                               outpufile='../data/kyiv_gp_data.csv',
                               types=['bar', 'restaurant'])
    
    # resp = google_places.nearby_search(
    #     lat_lng={'lat': 50.447514,
    #              'lng': 30.494205},
    #     radius=200,
    #     # type='restaurant'
    #     types=['bar']
    # )
    # results = resp.raw_response.get('results')
    # print(results[1])
    # for x in results:
    #     print(x['name'])

    # photo_ref = results[1]['photos'][0]['photo_reference']
    # a = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=2773&photoreference={photo_ref}&key={GP_API_KEY}'
    # print(a)
    # place_id = 'ChIJl9E5JovO1EARaU_OSDwxHqI'
    # detail_url_base = 'https://maps.googleapis.com/maps/api/place/details/output?'
    # det_res = requests.get(
    #     f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GP_API_KEY}&language=uk')
    # print(det_res.text)
    # print(det_res.url)
    # print(len(results))
    # for r in results:
    #     print(r['name'])
    #     print(r['geometry'])

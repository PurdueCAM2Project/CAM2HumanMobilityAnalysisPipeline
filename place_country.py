import json
import os
import pandas as pd



people_places = ['abbey',
                 'aquarium',
                 'crosswalk',
                 'beach',
                 'airplane_cabin',
                 'candy_store',
                 'butchers_shop',
                 'chapel',
                 'airport_terminal',
                 'alley',
                 'cathedral/outdoor',
                 'windmill',
                 'wet_bar',
                 'water_park',
                 'waiting_room',
                 'volleyball_court',
                 'coffee_shop',
                 'diner/outdoor',
                 'downtown',
                 'elevator/door',
                 'elevator/interior',
                 'elevator_lobby',
                 'train_railway',
                 'fastfood_restaurant',
                 'game_room',
                 'gazebo/exterior',
                 'gas_station',
                 'general_store/indoor',
                 'general_store/outdoor',
                 'gift_shop',
                 'gymnasium/indoor',
                 'ice_skating_rink/indoor',
                 'ice_skating_rink/outdoor',
                 'lavatory',
                 'train_interior',
                 'track/outdoor',
                 'toyshop',
                 'tower',
                 'ticket_booth',
                 'throne_room',
                 'temple/east_asia',
                 'temple/south_asia',
                 'synagogue/outdoor',
                 'train_station/platform',
                 'campus',
                 'sushi_bar',
                 'supermarket',
                 'subway_station/platform',
                 'street',
                 'baseball_field',
                 'movie_theater/indoor',
                 'skyscraper',
                 'ski_resort',
                 'ski_lodge',
                 'shopping_mall/indoor',
                 'shopfront',
                 'shoe_shop',
                 'restaurant_patio',
                 'auditorium',
                 'church/indoor',
                 'church/outdoor',
                 'restaurant_kitchen',
                 'restaurant',
                 'reception',
                 'pub/indoor',
                 'reading_room',
                 'recreation_room',
                 'rope_bridge',
                 'schoolhouse',
                 'science_museum',
                 'putting_green',
                 'stadium/baseball',
                 'stadium/football',
                 'stadium/soccer',
                 'stage/indoor',
                 'promenade',
                 'pulpit',
                 'pizzeria',
                 'pier',
                 'picnic_area',
                 'physics_laboratory',
                 'pharmacy',
                 'plaza',
                 'pet_shop',
                 'pavilion',
                 'parlor',
                 'mosque/outdoor',
                 'ballroom',
                 'office_buildings',
                 'medina',
                 'market/indoor',
                 'motel',
                 'museum/indoor',
                 'museum/outdoor',
                 'mausoleum',
                 'market/outdoor',
                 'lobby',
                 'loading_dock',
                 'lecture_room','laundromat',
                 'jewelry_shop',
                 'ice_cream_parlor',
                 'harbor',
                 'hallway',
                 'staircase',
                 'hardware_store',
                 'heliport',
                 'corridor']

vehicle_places = ['highway',
                  'raceway',
                  'desert_road',
                  'field_road',
                  'forest_road',
                  'crosswalk',
                  'gas_station',
                  'mountain_path']






def filter_by_place(places=None):
    combined_dictionary = {}
    if places is None:
        with open('classifications_real.json', 'r') as json_file:
            places = json.load(json_file)
    camera_database = pd.read_csv('camera_database.csv')
    cam_count = 0
    close_call_count = 0
    vehicle_count = 0
    people_count = 0
    both_count = 0
    for index, row in camera_database.iterrows():
        cam_id = row['_id/$oid'] + '/'
        if cam_id == 'l/':
            # bugged
            continue
        cam_count += 1

        #print(cam_id)
        #print(cam_count)
        country = row['country']
        highest_conf = -1
        highest_place = ''
        second_conf = -1
        second_place = ''        

        for place in places[cam_id].keys():
            if places[cam_id][place][0] * places[cam_id][place][1] > highest_conf: 
                highest_conf = places[cam_id][place][0] * places[cam_id][place][1]
                highest_place = place
            elif places[cam_id][place][0] * places[cam_id][place][1] > second_conf:
                second_conf = places[cam_id][place][0] * places[cam_id][place][1]
                second_place = place

        if (highest_conf - second_conf) < .001:
            close_call_count += 1
            #print('highest confidence: ', highest_conf)
            #print('highest place: ', highest_place)
            #print('second confidence: ', second_conf)
            #print('second place: ', second_place)

        if country == 'USA':
            country += ',' + row['state']


        if((highest_place in vehicle_places or second_place in vehicle_places) and
           (highest_place in people_places or second_place in people_places)):
            both_count += 1
            combined_dictionary[cam_id[:-1]] = ['both' , country]
            continue
            
        if(highest_place in vehicle_places or second_place in vehicle_places):
            vehicle_count += 1
            combined_dictionary[cam_id[:-1]] = ['vehicle' , country]
        
        if(highest_place in people_places or second_place in people_places):
            people_count += 1
            combined_dictionary[cam_id[:-1]] = ['people' , country]
            
        

    print('people count: ', people_count)
    print('vehicle count: ', vehicle_count)
    print('both count: ', both_count)
       
    with open("combined2021allcamerasReallyRealActual.json", "w") as f:
        json.dump(combined_dictionary, f)
    return combined_dictionary
    



if __name__ == '__main__':
    filter_by_place()

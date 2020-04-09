import sys
import pprint
import json
import datetime
import os

sys.path.insert(0, '../')

import k2kparser.den as pd

def is_today(day_tag):
    date_month = day_tag.replace('月', ',').replace('日', '').split(',')
    day_data = datetime.date(datetime.date.today().year, int(date_month[0]), int(date_month[1]))

    if (day_data - datetime.date.today()).days == 0:
        return True

    return False

def find_day(cached, tag):
    for day in cached:
        print(day)
        if day['day'] == tag:
            return day

    return None

def find_kaisai(cached, day_tag, place_tag):
    day_data = find_day(cached, day_tag)
    if day_data is None:
        return None

    for kaisai in day_data['places']:
        if kaisai['place'] == place_tag:
            return kaisai

    return None

def find_race(kaisai_cache, param):
    if kaisai_cache is None:
        return None

    for race in kaisai_cache['race']:
        if race['id'] == param:
            return race

    return None





def retrieve_kaisai_top():
    p = pd.ParserDenTop('/JRADB/accessD.html', 'pw01dli00/F3')
    kaisai_list = p.parse()

    kaisai_data = []

    pprint.pprint(kaisai_list)

    cached = None
    if os.path.exists('data/den.json'):
        with open('data/den.json', 'r') as f:
            cached = json.load(f)


    for day in kaisai_list:

        # day = find_day(cached, day['date'])
        # if day is not None:
        #     pass

        kaisai_day_data = {}
        kaisai_day_data['places'] = []

        all_finished = True

        for kaisai in day['kaisai']:
            kaisai_cache = find_kaisai(cached, day['date'], kaisai['place'])
            print(kaisai_cache)
            if kaisai_cache is not None and kaisai_cache['finish'] == True:
                kaiday_place_data = kaisai_cache
                kaisai_day_data['places'].append(kaiday_place_data)
            else:
                kaiday_place_data = {}
                kaiday_place_data['day'] = kaisai['day']
                kaiday_place_data['index'] = kaisai['index']
                kaiday_place_data['place'] = kaisai['place']
                kaisai_day_data['places'].append(kaiday_place_data)
                pk = pd.ParserDenKaisai(kaisai['param']['url'], kaisai['param']['param'])
                result = pk.parse()
                pprint.pprint(result)
                kaiday_place_data['race'] = races = []

                for race in result['races']:
                    race_cache = find_race(kaisai_cache, race['param']['param'])
                    if race_cache is None:
                        if race_cache['finish'] == True:
                            races.append(race_cache)
                            continue

                    else:
                        pr = pd.ParserDenRace('/JRADB/accessD.html', race['param']['param'])
                        race_detail = pr.parse()
                        if 'result' in race_detail:
                            finish = True
                        else:
                            all_finished = finish = False

                    races.append({
                        'id' : race['param']['param'],
                        'idx' : race['index'],
                        'cond': race['cond'],
                        'course': race['course'],
                        'departure': race['departure'],
                        'distance': race['dist'],
                        'name': race['name'],
                        'uma_num': race['uma_num'],
                        'finish': finish
                    })

                    file_name = 'data/races/' + race['param']['param'].replace('/', '-') + '.json'
                    with open(file_name, 'w') as f:
                        json.dump(race_detail, f, indent=4)
            #         pprint.pprint(race)

                kaiday_place_data['finish'] = all_finished

        print('{} : today ? {}'.format(day['date'], is_today(day['date'])))

        kaisai_day_data['day'] = day['date']


        kaisai_data.append(kaisai_day_data)


    with open('data/den.json', 'w') as f:
        json.dump(kaisai_data, f, indent=4 )



if __name__ == '__main__':
    retrieve_kaisai_top()



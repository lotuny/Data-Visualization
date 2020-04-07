from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import time


def get_all_neighbourhoods():
    driver.get("https://data.police.uk/api/metropolitan/neighbourhoods")
    return json.loads(driver.find_element_by_tag_name('pre').text)


def create_dict(neighbourhoods):
    final_dict = {}
    for i in range(len(neighbourhoods)):
        id = neighbourhoods[i].get('id')
        final_dict[id] = neighbourhoods[i]
        final_dict[id]['crime'] = {}
    return final_dict


def locate_crime_neighbourhood_id(latitude, longitude):
    driver.get("https://data.police.uk/api/locate-neighbourhood?q=" + latitude + "," + longitude + "")
    try:
        neighbourhood = json.loads(driver.find_element_by_tag_name('pre').text)
        return neighbourhood.get('neighbourhood')
    except:
        return 'Not Found'


def fill_dict(final_dict, data_file, start_row, row_num):
    file = data_file
    count = -1
    with open(file) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            count += 1
            if count < start_row:
                continue
            if count >= start_row+row_num:
                break
            latitude = row.get('Latitude')
            longitude = row.get('Longitude')
            month = row.get('Month')
            crime_type = row.get('Crime type')
            id = locate_crime_neighbourhood_id(latitude, longitude)
            item = final_dict.get(id)
            if item is not None:
                print('Line ' + str(count) + ': ' + str(id))
                if item.get('crime').get(month) is None:
                    item.get('crime')[month] = {
                        'Anti-social behaviour': 0,
                        'Bicycle theft': 0,
                        'Burglary': 0,
                        'Criminal damage and arson': 0,
                        'Drugs': 0,
                        'Other theft': 0,
                        'Possession of weapons': 0,
                        'Public order': 0,
                        'Robbery': 0,
                        'Shoplifting': 0,
                        'Theft from the person': 0,
                        'Vehicle crime': 0,
                        'Violence and sexual offences': 0,
                        'Other crime': 0,
                        'All crime': 0
                    }
                if item.get('crime')[month][crime_type] is not None:
                    item.get('crime')[month][crime_type] += 1
                else:
                    item.get('crime')[month]['Other crime'] += 1
                item.get('crime')[month]['All crime'] += 1
                file_path = "./data_set_in_neighbourhoods.json"
                file = open(file_path, "w", encoding='utf-8')#
                file.write(json.dumps(final_dict))
                file.close()
    fh.close()
    return final_dict


def load_dict_from_json(file_path):
    with open(file_path) as f:
        content = json.load(f)
        return content


chrome_options = Options()
driver = webdriver.Chrome(executable_path='./chromedriver',
                          chrome_options=chrome_options)
# neighbourhoods = get_all_neighbourhoods()  # neighbourhoods in metropolitan
# final_dict = create_dict(neighbourhoods)

start = time.perf_counter()
# final_dict = fill_dict(final_dict, 'metro_data/2020-02/2020-02-metropolitan-street.csv', 0, 1000)
test_dict = load_dict_from_json('data_set_in_neighbourhoods.json')
final_dict = fill_dict(test_dict, 'metro_data/2020-02/2020-02-metropolitan-street.csv', 22000, 80000)
end = time.perf_counter()
print('Duration: ' + str(end-start) + 's')

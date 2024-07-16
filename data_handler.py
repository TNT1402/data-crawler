import json
from crawler import fetch_data_from_url, parse_phone_info_data, parse_phone_category_data
from database import save_to_db

def crawl_data():
    # get all phone categories first
    category_url = 'https://www.thegioididong.com/dtdd' 
    html_phone_categories = fetch_data_from_url(category_url)
    if html_phone_categories:
        # parse phone category from html content
        phone_categories = parse_phone_category_data(html_phone_categories)

        phone_info_json = {}
        base_url = 'https://www.thegioididong.com/'
        suffix = '#c=42&m=2&o=17&pi=1'
        # with earch category, get detail content and parse necessary info
        for phone_category in phone_categories:
            phone_detail_url = base_url + phone_category + suffix
            html_phone_list_content = fetch_data_from_url(phone_detail_url)
            data = parse_phone_info_data(html_phone_list_content, phone_category)
            phone_info_json.update(data)

        save_to_json(phone_info_json, 'phone_info.json')
        print('save data to json successfully!')

def save_phone_info(connection):
    data = load_data_from_json('phone_info.json')
    if data:
        save_to_db(connection, data)

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
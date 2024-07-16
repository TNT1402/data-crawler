import requests
from bs4 import BeautifulSoup

def fetch_data_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check if request fail
         # save content to file
        with open("response", 'w', encoding='utf-8') as file:
            file.write(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def parse_phone_info_data(html_content, category):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []

    # find tag <ul class="listproduct">
    ul_tag = soup.find('ul', class_='listproduct')

    # if not found <ul class="listproduct">, return
    if not ul_tag:
        print("not found <ul class='listproduct'>")
        return {category: data}

    current_item = {}

    # browse through all <li> cards in the card <Ul Class = "Listproduct">
    for li_tag in ul_tag.find_all('li', class_='item'):
        current_item = {}

        # extract info from tag <h3>
        h3_tag = li_tag.find('h3')
        if h3_tag:
            current_item['title'] = h3_tag.get_text(strip=True)

        # extract src from tag <img>
        img_tag = li_tag.find('img')
        if img_tag:
            current_item['img_src'] = img_tag.get('src', '')

        # extract href from tag <a>
        a_tag = li_tag.find('a', class_='main-contain')
        if a_tag:
            href = "https://www.thegioididong.com" + a_tag.get('href', '')
            current_item['link_href'] = href

        # extract price from tag <strong> in tag <a>
        strong_tag = li_tag.find('strong', class_='price')
        if strong_tag:
            current_item['price'] = strong_tag.get_text(strip=True)

        data.append(current_item)
    # remove empty record
    filtered_data = [item for item in data if item]

    # set filtered_data to key category
    result = {category: filtered_data}
    return result

def parse_phone_category_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # find tag div
    div_tag = soup.find_all('div', class_='lst-quickfilter')
    phone_categories = []
    # if not found, return
    if not div_tag:
        print("not found <div class='lst-quickfilter'>")
        return phone_categories

    # browse through all sub tag of div tag
    for tag in div_tag:
        # if meet close tag div, stop loop for
        if tag.name == 'div' and tag.get('class') == ['lst-quickfilter'] and tag != div_tag:
            break
        a_tags = tag.find_all('a')
        for a_tag in a_tags:
            data_href = a_tag.get('data-href')
            if data_href:
                phone_categories.append(data_href)
    return phone_categories
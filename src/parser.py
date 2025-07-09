from bs4 import BeautifulSoup
import requests


def is_multipage(full_page) -> bool:
    paginator = full_page.find('div', class_='block-outer-main')

    return paginator != None


def get_last_full_page(url):
    response = requests.get(url)
    full_page = BeautifulSoup(response.text, 'html.parser')

    if is_multipage(full_page):
        last_page_url = 'https://proxima-rp.ru' + full_page.find_all('li', class_='pageNav-page')[-1].find('a').get('href')
        last_page_response = requests.get(last_page_url)
        last_full_page = BeautifulSoup(last_page_response.text, 'html.parser')

        return last_full_page
    return full_page


def parse_author_name_of_last_message(full_page):
    last_message_author_name = full_page.find_all('article', class_='message')[-1].get('data-author')
    
    return last_message_author_name


def parse_message_quantity(full_page):
    """
    Метод парсит количество сообщений в топике
    """
    messages_in_page: int = len(full_page.find_all('article', class_='message'))

    if is_multipage(full_page):
        last_page_number: int = int(full_page.find_all('li', class_='pageNav-page')[-1].text)
        message_quantity = (last_page_number - 1) * 20 + messages_in_page

        return message_quantity
    return messages_in_page


def get_full_info(url):
    full_page = get_last_full_page(url)

    return {'message_quantity': parse_message_quantity(full_page),
            'last_message_author_name': parse_author_name_of_last_message(full_page)}


url = 'https://proxima-rp.ru/threads/lost-opportunities-t-l-m-c.59267/page-7'

print(get_full_info(url))
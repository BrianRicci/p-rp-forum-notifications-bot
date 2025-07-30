from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp

import database.requests as rq


async def is_multipage(full_page) -> bool:
    """
    Проверка, много ли страниц у топика
    """
    paginator = full_page.find('div', class_='block-outer-main')

    return paginator != None


async def get_last_full_page(session, url):
    """
    Парсинг последней страницы
    """
    async with session.get(url) as response:
        response_text = await response.text()

        full_page = BeautifulSoup(response_text, 'html.parser')

        if not await is_multipage(full_page):
            return full_page
        
    last_page_url = 'https://proxima-rp.ru' + (full_page.find_all('li', class_='pageNav-page')[-1].find('a').get('href'))
    
    async with session.get(last_page_url) as response:
        last_page_response_text = await response.text()
        last_full_page = BeautifulSoup(last_page_response_text, 'html.parser')

        return last_full_page
        


async def parse_author_name_of_last_message(full_page):
    """
    Парсит имя автора последнего сообщения
    """
    last_message_author_name = (full_page
                                .find_all('article', class_='message')[-1]
                                .get('data-author'))
    
    return last_message_author_name


async def parse_message_quantity(full_page):
    """
    Функция парсит количество сообщений в топике
    """
    messages_in_page: int = len(full_page
                                .find_all('article', class_='message'))

    if await is_multipage(full_page):
        last_page_number: int = int(full_page
                                    .find_all('li', class_='pageNav-page')[-1]
                                    .text)
        message_quantity = (last_page_number - 1) * 20 + messages_in_page

        return message_quantity
    return messages_in_page


async def parse_topic_name(full_page):
    """
    Функция парсит название топика
    """
    h1 = full_page.find('h1', class_='p-title-value')
    
    for span in h1.find_all('span'):
        span.decompose()

    topic_name = h1.get_text(strip=True).replace('\xa0', ' ')
    
    return topic_name

# вынести это всё в другую функцию, которая сразу все в БД обновляет и делает рассылку в телеге
# а саму эту функцию оставить для использования еще при добавлении
async def get_full_info(session, url):
    """Получить все данные одного топика"""

    full_page = await get_last_full_page(session, url)
    
    print({'topic_name': await parse_topic_name(full_page),
            'message_quantity': await parse_message_quantity(full_page),
            'last_message_author_name': await parse_author_name_of_last_message(full_page)})
    # return {'topic_name': await parse_topic_name(full_page),
    #         'message_quantity': await parse_message_quantity(full_page),
    #         'last_message_author_name': await parse_author_name_of_last_message(full_page)}


async def gather_data():
    topics = await rq.get_topic_list()

    async with aiohttp.ClientSession() as session:
        tasks = list()

        for topic in topics:
            task = asyncio.create_task(get_full_info(session, topic.url))
            tasks.append(task)
        
        await asyncio.gather(*tasks)


url = 'https://proxima-rp.ru/threads/lost-opportunities-t-l-m-c.59267/page-7'

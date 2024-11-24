import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
import locale
from functools import cmp_to_key
from sortedcontainers import SortedDict

URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom='


# async def count_animals(page_from, session):
#     '''
#     problem: if we take words starting with the letter “Е” from wikipedia,
#     it will give us the names “обыкновенный ёж” and a couple more types starting with the letter “Ё”
#     the current implementation will consider them to be words starting with "О" and "Ё" respectively instead of "е"
#     '''
#     while True:
#         response = await session.get(URL + page_from)
#         if response.status == 200:
#             soup = BeautifulSoup(await response.text(encoding='UTF-8'), "html.parser")
#             div = soup.find(id='mw-pages').find('div', class_='mw-category-group')
#
#             # if letter of category don't match to page_from, return.
#             # otherwise words starting with a different letter will be counted again
#             h3 = div.find('h3')
#             if h3.text != page_from[0].upper():
#                 return
#
#             li = div.find_all('li')
#             animal_types = [l.text for l in li]
#
#             # remove type of animal that has already been calculated in previous call
#             if page_from in animal_types:
#                 animal_types.remove(page_from)
#
#             for animal_type in animal_types:
#                 animals[animal_type[0]] = animals.get(animal_type[0], 0) + 1
#             if len(animal_types) > 0:
#                 page_from = animal_types[-1]
#             else:
#                 return
#         else:
#             raise ConnectionError

async def count_animals(page_from, session):
    '''
    problem: if we take words starting with the letter “Е” from wikipedia,
    it will give us the names “обыкновенный ёж” and a couple more types starting with the letter “Ё”
    the current implementation will consider them to be words starting with "Е"
    '''
    while True:
        response = await session.get(URL + page_from)
        if response.status == 200:
            soup = BeautifulSoup(await response.text(encoding='UTF-8'), "html.parser")
            div = soup.find(id='mw-pages').find('div', class_='mw-category-group')

            # if letter of category don't match to page_from, return.
            # otherwise words starting with a different letter will be counted again
            h3 = div.find('h3')
            if h3.text != page_from[0].upper():
                return

            li = div.find_all('li')
            animal_types = [l.text for l in li]

            # remove type of animal that has already been calculated in previous call
            if page_from in animal_types:
                animal_types.remove(page_from)

            animals[page_from[0]] = animals.get(page_from[0], 0) + len(animal_types)
            if len(animal_types) > 0:
                page_from = animal_types[-1]
            else:
                return
        else:
            raise ConnectionError


if __name__ == '__main__':
    animals = {}


    async def async_gather():
        start = time.time()
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(ord('А'), ord('Я') + 1):
                tasks.append(asyncio.create_task(count_animals(chr(i), session)))
            await asyncio.gather(*tasks)

        locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')
        sorted_animals = SortedDict(cmp_to_key(locale.strcoll), animals)

        with open('beasts.csv', 'w') as file:
            for key, value in sorted_animals.items():
                file.write(f'{key},{value}\n')

        print(sorted_animals)
        print(time.time() - start)

    asyncio.run(async_gather())

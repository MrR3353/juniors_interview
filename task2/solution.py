import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom='


async def count_animals(startswith: str, session: aiohttp.ClientSession):
    '''
    if we take words starting with the letter “Е” from wikipedia,
    it will give us the names “обыкновенный ёж” and a couple more types starting with the letter “Ё”
    the current implementation will consider them to be words starting with "Е"
    '''
    count = 0
    page_from = startswith
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

            count += len(animal_types)
            if len(animal_types) > 0:
                page_from = animal_types[-1]
            else:
                return startswith, count
        else:
            raise ConnectionError


async def get_all_animals():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(ord('А'), ord('Я') + 1):
            tasks.append(asyncio.create_task(count_animals(chr(i), session)))
        animals_by_letters = await asyncio.gather(*tasks)
    animals_by_letters = {animal[0]: animal[1] for animal in animals_by_letters if animal is not None}
    return animals_by_letters


if __name__ == '__main__':
    start = time.time()
    animals = asyncio.run(get_all_animals())
    print(animals)
    with open('beasts.csv', 'w') as file:
        for key, value in animals.items():
            file.write(f'{key},{value}\n')
    print(time.time() - start)

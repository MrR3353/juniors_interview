import threading
import time
import requests
from bs4 import BeautifulSoup
import locale
from functools import cmp_to_key
from sortedcontainers import SortedDict

URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom='


def count_animals(page_from, session):
    while True:
        # with requests.session() as session:
            response = session.get(URL + page_from)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
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

                with lock:
                    # if we take words starting with the letter “Е” from wikipedia,
                    # it will give us the names “обыкновенный ёж” and a couple more types starting with the letter “Ё”
                    # the current implementation will consider them to be words starting with "О" and "Ё" respectively instead of "е"
                    # for animal_type in animal_types:
                    #     animals[animal_type[0]] = animals.get(animal_type[0], 0) + 1
                    animals[page_from[0]] = animals.get(page_from[0], 0) + len(animal_types)
                if len(animal_types) > 0:
                    page_from = animal_types[-1]
                else:
                    return
            else:
                raise ConnectionError


if __name__ == '__main__':
    start = time.time()
    threads = []
    animals = {}
    lock = threading.Lock()
    with requests.session() as session:
        for i in range(ord('А'), ord('Я') + 1):
            thread = threading.Thread(target=count_animals, args=(chr(i), session))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')
    sorted_animals = SortedDict(cmp_to_key(locale.strcoll), animals)

    with open('beasts.csv', 'w') as file:
        for key, value in sorted_animals.items():
            file.write(f'{key},{value}\n')

    print(sorted_animals)
    print(time.time() - start)

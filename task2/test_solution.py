import aiohttp
import pytest
import requests
from aioresponses import aioresponses

import solution
import solution2



@pytest.mark.asyncio
async def test_count_animals_success():
    letter = 'А'
    initial_url = solution.URL + letter
    next_url = solution.URL + 'Антилопа'

    with aioresponses() as m:
        # Mock the first response
        m.get(initial_url, status=200, body='''
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>А</h3>
                <ul>
                    <li>Аист</li>
                    <li>Антилопа</li>
                </ul>
            </div>
        </div>
        ''', headers={'Content-Type': 'text/html; charset=UTF-8'})

        # Mock the second response
        m.get(next_url, status=200, body='''
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>А</h3>
                <ul>
                    <li>Антилопа</li>
                </ul>
            </div>
        </div>
        ''', headers={'Content-Type': 'text/html; charset=UTF-8'})

        async with aiohttp.ClientSession() as session:
            result = await solution.count_animals(letter, session)

    assert result == ('А', 2), "Count for letter А should be 2"


@pytest.mark.asyncio
async def test_count_animals_wrong_letter():
    letter = 'Б'
    mock_url = solution.URL + letter

    # Mock the HTTP response
    with aioresponses() as m:
        html_content = '''
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>В</h3>
                <ul>
                    <li>Волк</li>
                </ul>
            </div>
        </div>
        '''
        m.get(mock_url, status=200, body=html_content, headers={'Content-Type': 'text/html; charset=UTF-8'})

        async with aiohttp.ClientSession() as session:
            result = await solution.count_animals(letter, session)

    assert result is None, "If the letter does not match, the result should be None"


@pytest.mark.asyncio
async def test_compare_solutions():
    for i in range(ord('У'), ord('Ф') + 1):
        async with aiohttp.ClientSession() as session:
            count = await solution.count_animals(chr(i), session)
        with requests.session() as session:
            count2 = solution2.count_animals(chr(i), session)
        assert count == count2, f"Count of animals on '{chr(i)}'"
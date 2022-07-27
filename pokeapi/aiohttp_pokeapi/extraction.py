import datetime
import aiohttp
import asyncio
from bs4 import BeautifulSoup


P_MAIN_URL = 'https://pokemondb.net{}'

async def get_page(session, url):
    async with session.get(url) as r:
        return await r.text()

async def get_all(session, urls):
    print(f'[!] Creating tasks')
    tasks = list()
    for url in urls:
        tasks.append(asyncio.create_task(get_page(session, url)))
    responses = await asyncio.gather(*tasks)
    return responses

async def get_pokedex(response):
    data = dict()
    bs = BeautifulSoup(response, features='html.parser')
    data['name'] = bs.find('h1').text
    data['id'] = bs.find('th', string='National №').find_next_sibling('td').find('strong').text
    data['type'] = [a.text for a in bs.find('th', string='Type').find_next_sibling('td').find_all('a')]
    data['species'] = bs.find('th', string='Species').find_next_sibling('td').text
    data['height'] = bs.find('th', string='Height').find_next_sibling('td').text
    data['weight'] = bs.find('th', string='Weight').find_next_sibling('td').text
    return data

async def get_data(responses):
    print(f'[!] Getting data...')
    tasks = list()
    for response in responses:
        tasks.append(asyncio.create_task(get_pokedex(response)))
    data = await asyncio.gather(*tasks)
    return data

async def main():
    urls = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'\
            ' Chrome/102.0.0.0 Safari/537.36'
    }
    pokemon_responses = None
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://pokemondb.net/pokedex/all') as response:
            print(f'[!] Extracting tags')
            bs = BeautifulSoup(await response.text(), features='html.parser')
        urls = list(set([P_MAIN_URL.format(a['href']) for a in bs.find_all('a', class_='ent-name')]))
        pokemon_responses = await get_all(session, urls)
    print(f'[!] Extracting data for 100 pokemons')
    return await get_data(pokemon_responses[0:100])


if __name__ == '__main__':
    start = datetime.datetime.now()
    data = asyncio.get_event_loop().run_until_complete(main())
    exec_time = (datetime.datetime.now() - start)
    print(f'extracted in {exec_time} seconds')
import json, aiohttp, asyncio
from bs4 import BeautifulSoup

async def get_movie_info(url):
    try:
        headers = {
            'Cookie': 'PHPSESSID=275296288d7d0dde8f5381eca89a4fe9; senpainoticeme=15967'
        }
        download_links = []
        myDict = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                name = soup.find(itemprop="name").text
                description = soup.find(itemprop="description").text.strip()
                thumbnail_url = soup.find('meta', itemprop='thumbnail')['content']

                download_list = soup.find('div', class_="download-list d-hidden")
                if download_list:
                    links = download_list.find_all('a')
                    for link in links:
                        if link.text != "Telegram orqali yuklash olish":
                            myDict[link.text.replace('Скачать ', '')] = link['href']
                download_links.append({"name": name, "description": description, "thumbnail": thumbnail_url, "results": myDict})
        return download_links
    except:
        return False


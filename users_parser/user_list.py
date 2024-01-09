import asyncio
from pprint import pprint

import aiohttp
import aiofiles
import requests
from lxml import etree, html

from users_parser.main import BaseAsyncParse
from bs4 import BeautifulSoup


async def get_users(page_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "identity;q=1, *;q=0"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://dublikat.club/members/list/?page={page_number}", headers=headers) as response:
            text = await response.text("utf-8")
            async with aiofiles.open(f'htmls/page_{page_number}.html', 'w') as f:
                await f.write(text)


class UserList(BaseAsyncParse):
    async def get_usernames(self, count_query: int = 100):
        text = await self.aget_page_source(self.base_url)
        count_pages: int = self.get_count_pages(text)
        count_iterations: int = (count_pages // count_query) + 1
        pages_list = list(range(1, count_pages + 1))
        usernames = []
        for i in range(count_iterations):
            print(f'Итерация номер - {i+1}')
            part_list = pages_list[count_query * i: i * count_query + count_query]
            part_usernames = await self.get_part_usernames(part_list)
            usernames.extend(part_usernames)

        async with aiofiles.open('users_list.txt', 'a') as f:
            for username in usernames:
                await f.write(username + '\n')

    async def get_part_usernames(self, page_numbers: list):
        tasks = []
        for num in page_numbers:
            tasks.append(asyncio.create_task(self.aget_page_source(self.base_url + f'?page={num}')))
        texts = await asyncio.gather(*tasks)

        usernames = []
        for text in texts:
            usernames.extend(
                self.parse_usernames(text)
            )
        return usernames

    def parse_usernames(self, page_sourse: str):
        soup = BeautifulSoup(page_sourse, 'lxml')
        usernames = []
        for username in soup.find_all('a', {'class': 'username'}):
            usernames.append(username.text)
        return usernames

    @staticmethod
    def get_count_pages(page_source):
        tree = html.fromstring(page_source)
        result = tree.xpath("/html/body/div[1]/div[4]/div/div[3]/div[2]/div/div/div[2]/nav/div[1]/ul/li[5]")
        return int(result[0].text_content())


async def main():
    ul = UserList("https://dublikat.club/members/list/")
    result = await ul.get_usernames()
    pprint(result)


if __name__ == '__main__':
    asyncio.run(main())
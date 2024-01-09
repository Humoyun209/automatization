import asyncio
import random
import re
from fake_useragent import UserAgent

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup

from users_parser.main import BaseAsyncParse


class TelegramLink(BaseAsyncParse):
    async def aget_url_ads(self):
        text = await self.aget_page_source(self.base_url)
        count_pages = self.get_count_pages(text)
        tasks = []
        for i in range(count_pages):
            tasks.append(asyncio.create_task(self.aget_page_source(self.base_url + f'page-{i+1}')))
        texts = await asyncio.gather(*tasks)
        urls = []
        for text in texts:
            urls.extend(self.parse_url_ads(text))
        return urls

    async def aget_links_tg(self):
        ad_urls = await self.aget_url_ads()
        ad_urls = ad_urls
        tasks = []
        for url in ad_urls:
            tasks.append(asyncio.create_task(self.aget_page_source(url)))
        texts = await asyncio.gather(*tasks)
        tg_links = []
        for i, text in enumerate(texts):
            print(f'Получение телеграм с {i + 1}')
            page_urls = self.parse_telegram_links(text)
            tg_links.extend(page_urls)
        return tg_links

    async def awrite_to_file(self):
        tg_links = await self.aget_links_tg()
        tg_links = list(set(tg_links))
        async with aiofiles.open(f'telegrams_txt/{self.base_url.split("/")[-2]}', 'a') as f:
            for link in tg_links:
                await f.write(link + '\n')

    def get_count_pages(self, page_source):
        soup = BeautifulSoup(page_source, "lxml")
        ul = soup.find('ul', {'class': 'pageNav-main'})
        page_numbers = len(ul.find_all('li'))
        return page_numbers

    def parse_url_ads(self, page_source):
        urls = []
        soup = BeautifulSoup(page_source, "lxml")
        ads = soup.find_all('div', {'class': ['structItem', 'structItem--thread']})
        for ad in ads:
            res = ad.find('a', href=re.compile("/threads/"))
            url = res.get('href')
            urls.append(
                'https://dublikat.club' + url
            )
        return urls

    def parse_telegram_links(self, page_source):
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            content = soup.find('div', {'class': 'message-cell--main'})
            urls_with_sobachka = re.findall(r'\B@\w+', content.text)
            urls_tme = [link.get('href') for link in content.find_all('a', {'class': ['link', 'link--external']})
                        if link.get('href').startswith('https://t.me/')]
            urls_tme.extend(urls_with_sobachka)
            return urls_tme
        except Exception as e:
            return []


async def main():
    tl = TelegramLink("https://dublikat.club/forums/prodazha-sim-kart-i-prochie-uslugi.225/")
    await tl.awrite_to_file()


if __name__ == '__main__':
    asyncio.run(main())
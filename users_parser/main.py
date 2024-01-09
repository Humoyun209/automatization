import aiohttp
from fake_useragent import UserAgent


class BaseAsyncParse:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_headers(self):
        return {
            'User-Agent': UserAgent().random
        }

    async def aget_page_source(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.get_headers()) as response:
                return await response.text()
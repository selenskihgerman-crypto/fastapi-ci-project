import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os


class Crawler:
    def __init__(self, max_depth=3):
        self.visited = set()
        self.max_depth = max_depth
        self.external_links = set()
        self.session = None
        self.internal_links = set()

    async def fetch(self, url):
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Failed to fetch {url}: Status {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def is_external(self, url, base_url):
        base_domain = urlparse(base_url).netloc
        parsed_url = urlparse(url)
        return parsed_url.netloc != '' and parsed_url.netloc != base_domain

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for a in soup.find_all('a', href=True):
            href = a['href']
            # Пропускаем якорные ссылки и javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue

            absolute_url = urljoin(base_url, href)
            # Нормализуем URL
            parsed = urlparse(absolute_url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized_url += f"?{parsed.query}"

            links.add(normalized_url)

        return links

    async def crawl(self, url, depth=0):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)
        print(f"Crawling {url} at depth {depth}")

        html = await self.fetch(url)
        if not html:
            return

        links = self.extract_links(html, url)
        for link in links:
            if self.is_external(link, url):
                self.external_links.add(link)
                print(f"Found external link: {link}")
            else:
                if link not in self.visited:
                    self.internal_links.add(link)
                    await self.crawl(link, depth + 1)

    async def start(self, start_urls):
        async with aiohttp.ClientSession() as self.session:
            tasks = [self.crawl(url) for url in start_urls]
            await asyncio.gather(*tasks)

        # Сохраняем найденные внешние ссылки
        with open('external_links.txt', 'w', encoding='utf-8') as f:
            f.write("EXTERNAL LINKS FOUND:\n")
            f.write("=" * 50 + "\n")
            for link in sorted(self.external_links):
                f.write(f"{link}\n")

        # Сохраняем статистику
        with open('crawler_stats.txt', 'w', encoding='utf-8') as f:
            f.write("CRAWLER STATISTICS:\n")
            f.write("=" * 50 + "\n")
            f.write(f"Start URLs: {start_urls}\n")
            f.write(f"Max depth: {self.max_depth}\n")
            f.write(f"Total pages visited: {len(self.visited)}\n")
            f.write(f"Internal links found: {len(self.internal_links)}\n")
            f.write(f"External links found: {len(self.external_links)}\n")

        print(f"\nCrawling completed!")
        print(f"Visited {len(self.visited)} pages")
        print(f"Found {len(self.external_links)} external links")
        print(f"Results saved to external_links.txt and crawler_stats.txt")


async def main():
    print("Web Crawler started!")
    print("Enter starting URLs (comma separated):")
    urls_input = input().strip()
    start_urls = [url.strip() for url in urls_input.split(',') if url.strip()]

    print("Enter max depth (default 3):")
    depth_input = input().strip()
    max_depth = int(depth_input) if depth_input else 3

    crawler = Crawler(max_depth=max_depth)
    await crawler.start(start_urls)


if __name__ == "__main__":
    asyncio.run(main())
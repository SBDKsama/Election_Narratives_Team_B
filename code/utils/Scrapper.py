import threading

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Scrapper:
    def __init__(self, url):
        self.url = set()
        if type(url) == str:
            self.url.add(url)
        else:
            for u in url:
                self.url.add(u)
        self.result_map = {}
        self.progress_bar = None

    def get_one_content(self, url):
        resp = None
        try:
            resp = requests.get(url)
            if not resp.ok:
                self.result_map[url] = {'url': url, 'content': None, 'http_status': resp.status_code,
                                        'error': None, 'success': False}
                return self.result_map[url]
            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                self.result_map[url] = {'url': url, 'content': None, 'http_status': resp.status_code,
                                        'error': 'Non-HTML content', 'success': False}
                return self.result_map[url]
            resp_text = resp.text
            soup = BeautifulSoup(resp_text, 'html.parser')
            for script in soup(["script", "style", "img"]):
                script.decompose()
            text = soup.get_text(separator=' ', strip=True)

            import re
            text = re.sub(r'\s+', ' ', text)

            self.result_map[url] = {'url': url, 'content': text, 'http_status': resp.status_code, 'error': None,
                                    'success': True}
            return self.result_map[url]
        except Exception as e:
            self.result_map[url] = {'url': url, 'content': None, 'http_status': resp.status_code, 'error': str(e),
                                    'success': False}
            return self.result_map[url]

    def get_contents_thread(self):
        while True:
            url = None
            try:
                url = self.url.pop()
            except:
                pass
            if url is None:
                return
            try:
                self.get_one_content(url)
                if self.progress_bar is not None:
                    self.progress_bar.update(1)
            except:
                pass

    def get_all_contents(self, thread_num=5, show_progress=True):
        threads = []
        if show_progress:
            self.progress_bar = tqdm(total=len(self.url), desc="Scraping progress", ncols=100)
        for _ in range(thread_num):
            thread = threading.Thread(target=self.get_contents_thread)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        if show_progress:
            self.progress_bar.close()

import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        resp = None
        try:
            resp = requests.get(self.url)
            if not resp.ok:
                return {'url': self.url, 'content': None, 'http_status': resp.status_code,
                        'error': None, 'success': False}
            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                return {'url': self.url, 'content': None, 'http_status': resp.status_code,
                        'error': 'Non-HTML content', 'success': False}
            resp_text = resp.text
            soup = BeautifulSoup(resp_text, 'html.parser')
            for script in soup(["script", "style", "img"]):
                script.decompose()
            text = soup.get_text(separator=' ', strip=True)

            import re
            text = re.sub(r'\s+', ' ', text)

            return {'url': self.url, 'content': text, 'http_status': resp.status_code, 'error': None, 'success': True}
        except Exception as e:
            return {'url': self.url, 'content': None, 'http_status': resp.status_code,
                    'error': str(e), 'success': False}

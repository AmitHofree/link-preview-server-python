import requests
from bs4 import BeautifulSoup

CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

class WebScraper:
    def __init__(self, url, user_agent=CHROME_UA):
        self.url = url
        self.user_agent = user_agent
        self.soup = None

    def _get_content(self):
        r = requests.get(self.url, headers={'User-Agent': self.user_agent})
        if not r.ok:
            raise Exception(f"Received status - {r.status}")
        
        soup = BeautifulSoup(r.content, 'html.parser')
        self.soup = soup

    def getTitle(self):
        if not self.soup:
            self._get_content()

        if og_titles := self.soup.select('meta[property="og:title"]'):
            if og_title := og_titles[0]:
                return og_title["content"]
        if doc_title := self.soup.title:
            return doc_title.get_text()
        if h1s := self.soup.select('h1'):
            if h1 := h1s[0]:
                return h1.get_text()
        if h2s := self.soup.select('h2'):
            if h2 := h2s[0]:
                return h2.get_text()
        return ""
    
    def getDescription(self):
        if not self.soup:
            self._get_content()

        if og_descriptions := self.soup.select('meta[property="og:description"]'):
            if og_description := og_descriptions[0]:
                return og_description["content"]
        if meta_descriptions := self.soup.select('meta[name="description"]'):
            if meta_description := meta_descriptions[0]:
                return meta_description["content"]
        return ""

    def getImage(self):
        if not self.soup:
            self._get_content()

        if og_imgs := self.soup.select('meta[property="og:image"]'):
            if og_img := og_imgs[0]:
                return og_img["content"]
        if  img_rel_links := self.soup.select('link[rel="image_src"]'):
            if img_rel_link := img_rel_links[0]:
                return img_rel_link["href"]
        return ""

    def getPreview(self):
        return {
            "title": self.getTitle(),
            "description": self.getDescription(),
            "img": self.getImage()
        }
            

if __name__ == "__main__":
    import sys
    w = WebScraper(sys.argv[1])
    for key, value in w.getPreview().items():
        print(f"[{key}] - {value}")

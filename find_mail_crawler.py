import sys
import requests
import re
from bs4 import BeautifulSoup

TO_CRAWL = []
CRAWLED = set()
EMAILS = []

def request(link):
    #header = {'User-Agent': 'Mozilla/5.0'} #example
    try:
        response = requests.get(link)
        response.close()
        return response.text
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass


def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags_a_finded = soup.find_all('a', href=True)
        for tag in tags_a_finded:
            link = tag['href']
            if link.startswith('http'):
                links.append(link)
        return links

    except:
        pass


def get_emails(html):
    try:
        emails = re.findall(r'\w[\w\.]+\w@\w[\w\.]+\w', html)
        return emails
    except KeyboardInterrupt:
        sys.exit(0)


def crawl():
    while True:
        if TO_CRAWL:
            url = TO_CRAWL.pop()
            html = request(url)
            if html:
                links = get_links(html)
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL:
                            TO_CRAWL.append(link)

                emails = get_emails(html)
                for email in emails:
                    if email not in EMAILS:
                        print(f'email found! -> {email}')
                        EMAILS.append(email)
                CRAWLED.add(url)
            else:
                CRAWLED.add(url)
        else:
            print('Done!')
            break


if __name__ == '__main__':
    url = sys.argv[1]
    TO_CRAWL.append(url)
    crawl()
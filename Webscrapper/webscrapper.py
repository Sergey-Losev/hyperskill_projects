import requests
from bs4 import BeautifulSoup
import json
import string


def initial_request():
    user_url = input()
    r = requests.get(user_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r and 'content' in r.json():
        print(r.json()['content'])
    else:
        print(f'The URL returned {r.status_code}!')


def check_link():
    user_link = input()
    requests_link = requests.get(user_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(requests_link.content, 'html.parser')
    # check_movie = soup.find('script', type="application/ld+json").attrs
    check_movie = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
    print('Invalid movie page!')
    if check_movie['@type'] == 'Movie' or check_movie['@type'] == 'TVSeries':
        print({'title': check_movie['name'], 'description': check_movie['description']})
    else:
        print('Invalid movie page!')


def new_request():
    user_url = input('Input the URL:\n')
    r = requests.get(user_url)
    if r:
        with open('source.html', 'wb') as f:
            f.write(r.content)
        print('Content saved.')
    else:
        print(f'The URL returned {r.status_code}!')


def get_page_content(url):
    """requests all page content by url"""
    print(f"Requesting page content by URL: {url}")
    request = requests.get(url)
    if request.status_code != 200:
        print(f"Something went wrong, error: {request.status_code}")
        return False
    else:
        print("Done!")
        return request.content


def get_article_title(page):
    """return article title"""
    parsed = BeautifulSoup(page, 'html.parser')
    print("Getting article title...")
    title = parsed.title.string
    print("Done!")
    return title


def get_article_text(page):
    """get article text"""
    parsed = BeautifulSoup(page, 'html.parser')
    print("Getting article text...")
    text = parsed.find(class_="article__body cleared")
    print("Done!")
    return text.get_text()


def prepare_file_name(title):
    """Replace the whitespaces with underscores and remove punctuation marks in the filename
    (str.maketrans and string.punctuation will be useful for this). Also, strip all trailing whitespaces
     in the article title"""
    stripped_title = str(title).strip()
    trans_table = stripped_title.maketrans(' ', '_', string.punctuation)  # swap "space" with "undescore", "punctuation" with None
    return stripped_title.translate(trans_table) + '.txt'


def save_file(title, text):
    """saves file with article_title and article_text"""
    print("Saving to file")
    file = open(title, 'w', encoding='utf-8')
    file.write(text)
    file.close()
    print(f"File saved {title}")


def start():
    urls = []
    starting_url = 'https://www.nature.com/nature/articles/'
    r = get_page_content(starting_url)
    soup = BeautifulSoup(r, 'html.parser')
    all_articles = soup.find_all('article')
    for article in all_articles:
        if article.find(class_="c-meta__type").string == 'News':
            article_href = article.find(attrs={'data-track-action': 'view article'}).get('href')
            urls.append(f"https://www.nature.com{article_href}")
    for url in urls:
        print("-------------------------------------------")
        page_content = get_page_content(url)
        article_title = get_article_title(page_content)
        article_text = str(get_article_text(page_content)).strip()
        file_name = prepare_file_name(article_title)
        save_file(file_name, article_text)
        
        
if __name__ == "__main__":
    start()

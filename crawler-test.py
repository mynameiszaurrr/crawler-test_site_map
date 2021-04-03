from bs4 import BeautifulSoup
import requests

URL = 'http://crawler-test.com/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36 '
}


class RequestsForUrl(object):
    def __init__(self, urls, header):
        self.url = urls
        self.headers = header

    def requests_on_page(self):
        response = requests.get(url=self.url, headers=self.headers).text
        return response


class SiteParser(object):
    def __init__(self, html_site):
        self.site = html_site

    def first_level_names(self):
        soup = BeautifulSoup(self.site, 'lxml')
        h3_soup = soup.find_all('h3')
        return h3_soup

    def first_level_columns(self):
        soup = BeautifulSoup(self.site, 'lxml')
        tables_soup = soup.find_all('div', class_='large-4 columns')
        return tables_soup

    def title_name(self):
        soup = BeautifulSoup(self.site, 'lxml')
        return soup.title.text


class SiteLinks(object):
    def __init__(self, html_site):
        self.site = html_site

    def large_columns(self):
        soup = BeautifulSoup(self.site, 'lxml')
        columns = soup.find_all('div', class_='large-4 columns')
        return columns


site_response = RequestsForUrl(urls=URL, header=HEADERS).requests_on_page()
first_level = SiteParser(site_response).first_level_names()
first_column = SiteLinks(site_response).large_columns()
links = first_column
first_pars_link = str(links).split('<a href="')
links_list = []
for j in first_pars_link[1:]:
    second_pars_link = j.split('">')[0]
    if '"' in second_pars_link:
        second_pars_link = second_pars_link.split('"')[0]
    if second_pars_link[0] == '/' or second_pars_link[0] == '?':
        links_list.append('http://crawler-test.com' + second_pars_link)
    else:
        links_list.append(second_pars_link)


try:
    print(SiteParser(site_response).title_name())
    iteration_number = 0
    for i in range(0, 13):
        print(f'\t*{first_level[i].text}')
        for j in links_list:
            if f'/{first_level[i].text.lower().split()[0]}' in j:
                print(j)
except Exception as ex:
    print(f'Ошибка: {ex}')


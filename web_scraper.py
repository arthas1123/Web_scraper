import requests
from bs4 import BeautifulSoup
import pprint

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'])

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes':points})
    return sort_stories_by_votes(hn)



nh_home = "https://news.ycombinator.com/"
next_page = 2 # new?p=2 starting from page1 and after clicked, page2
current_page = nh_home
check_page = 5
total_links = []
total_subtext = []

for i in range(check_page):
    if i != 0:
        current_page = current_page + "news?p=" + str(next_page)
        next_page += 1
    response = requests.get(current_page)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    total_links += links
    total_subtext += subtext

customed_hn = create_custom_hn(total_links, total_subtext)

pprint.pprint(customed_hn)
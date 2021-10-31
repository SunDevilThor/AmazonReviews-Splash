# Amazon Reviews - Splash
# Tutorial from John Watson Rooney YouTube channel

import requests
from bs4 import BeautifulSoup
import pandas as pd

review_list = []

def get_soup(url):
    response = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try: 
        for item in reviews: 
            product = soup.title.text.replace('Amazon.com: Customer reviews: ', '').strip()
            title = item.find('a', {'data-hook': 'review-title'}).text.strip()
            rating = float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace(' out of 5 stars', '').strip())
            body = item.find('span', {'data-hook': 'review-body'}).text.strip()

            review = {
                'product' : product,
                'title': title, 
                'rating': rating, 
                'body': body,
            }

            review_list.append(review)
    except: 
        pass

for x in range(1, 25):
    print(f'Getting page: {x}')
    soup = get_soup(f'https://www.amazon.com/Sony-Full-Frame-Compact-Mirrorless-Camera/product-reviews/B08HVXJZYY/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    print(len(review_list))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(review_list)
df.to_csv('Amazon-Reviews.csv')
print('Saved items to CSV file.')


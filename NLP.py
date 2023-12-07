 '''rating the reading level of Wikipedia texts to be more general'''

import  requests # to contact widipedia
import json # to print json in an easy to see way
from bs4 import BeautifulSoup # to remove HTML
from textatistic import Textatistic

while True:
    1 # prompt the user to enter a wikipedia page title
    article_name = input('Please enter the name of an article, with_as spaces("quit" to exit):')
    if article_name == 'quit':
        break
    
    # make it title case
    # article_name = article_name.title()
    # replace spaces with_
    article_name = article_name.replace(' ','_')
        
    2 # go get the text from the page, as a json
    print('Making a request for the article {article_name}...')
    base_url = 'https://en.wikipedia.org/w/api.php?action=parse&page='
    url_ending = '&format=json'
    requested_url = base_url + article_name + url_ending
    response = requests.get(requested_url)
    print(response)
    
    #check the HTTP reponse was successful
    '''
    if response.status_code != 200:
        print(f'Error in request({response}). Please try again')
        continue
    '''
    
    3 # extract the items of interest from the page
    print('Analyzing text...')
    response_json_obj = response.json()
    json_str = json.dumps(response_json_obj, indent = 4)
    # print(json_str)

    #just look at the text part
    article_text_html = response_json_obj['parse']['text']['*']
    # print(article_text_html)

    #remove HTML 
    article_soup = BeautifulSoup(article_text_html, 'html.parser')
    article_plaintext = article_soup.get_text().replace('\n', ' ')
    print(article_plaintext)
    
    # 4 estimate the reading level of the page text
    readibility_obj = Textatistic(article_plaintext)
    print('=' * 60)
    print(f'Readability Gunnint Fog score: {readibility_obj.gunningfog_score:0.2f}')
    print(f'Readability Simple Measure of Gobbledygook score: {readibility_obj.smog_score:0.2f}')
    print(f'Readability Flesch-Kincaid score: {readibility_obj.fleschkincaid_score:0.2f}')

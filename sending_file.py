import urllib
import urllib.request
import xml.etree.ElementTree as ET

import requests


def send_a_pdf_to_api_and_get_text_from_api(file_url):
    local_file = 'local_copy.pdf'
    # it's the internal api 
    # is used to send pdf-file and get document_id
    post_url = "http://localhost:5000/documents"

    
    
    urllib.request.urlretrieve(pdf_url, local_file)
    
    files = {"file": open(local_file, "rb")}

    # send file
    response = requests.post(post_url, files=files)
    
    # api is configured to return documenet_id
    # get id of the document saved in database
    document_id = response.json()['id']

    # getting data from api
    get_url = "http://localhost:5000/text/"+str(document_id)+".txt"

    # the api is configured to return text when document_id is sent
    response = requests.get(get_url)
    # print(response.text['text'])
    text_from_file = response.json()

    return text_from_file['text']

# print(get_text_from_api('sample.pdf'))



# existing function
def get_article_data(url):
    # ex of API request
    # url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
    # url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=15'

    data = urllib.request.urlopen(url)
    # print(data.read().decode('utf-8'))

    tree = ET.parse(data)

    # putting article data in dictionary

    array_of_articles = []
    root = tree.getroot()
    # article_buffer = {}
    for child in root:

        article_buffer = {}
        art_authors = []
        for grand_child in child:

            # finds and updates article's link
            if grand_child.tag == '{http://www.w3.org/2005/Atom}id':
                article_link = grand_child.text
                pdf_link = article_link.replace(
                    'http://arxiv.org/abs', 'http://arxiv.org/pdf')
                article_buffer['pdf_link'] = pdf_link

            if grand_child.tag == '{http://www.w3.org/2005/Atom}title':
                article_buffer['title'] = grand_child.text

            if grand_child.tag == '{http://www.w3.org/2005/Atom}published':
                # in order to keep only the year
                article_buffer['published_on_date'] = grand_child.text[:4]

            if grand_child.tag == '{http://www.w3.org/2005/Atom}summary':
                article_buffer['summary'] = grand_child.text
            
            if grand_child.tag == '{http://arxiv.org/schemas/atom}comment':
                article_buffer['comment'] = grand_child.text
            
            if grand_child.tag == '{http://arxiv.org/schemas/atom}journal_ref':
                # we keep only the part related to the name of journal 
                # and don't keep page numbers
                journal_name_limiter = grand_child.text.find(')')
                journal_name = grand_child.text[:journal_name_limiter+1]
                article_buffer['journal_ref'] = journal_name
            
            # ::2 to avoid printing departments
            # for grand_grand_child in grand_child[::2]:
            author_dict = {}
            for grand_grand_child in grand_child:

                if grand_grand_child.tag == '{http://www.w3.org/2005/Atom}name':
                    writer = grand_grand_child.text
                    author_dict['name'] = writer
                    # print(writer)
                
                # some responses provide information on author's lab
                if grand_grand_child.tag == '{http://arxiv.org/schemas/atom}affiliation':
                    lab_of_writer = grand_grand_child.text
                    # print(lab_of_writer)
                    author_dict['lab'] = lab_of_writer
                    # print(lab_of_writer)
                
            # fill in the list of authors (each author is a dictionary with name and lab of the author)
            if author_dict:
                art_authors.append(author_dict)

            if article_buffer:
                article_buffer['authors'] = author_dict
            
            if len(art_authors) > 0:
                article_buffer['authors'] = art_authors
            
        # if dictionary is empty
        if article_buffer:
            array_of_articles.append(article_buffer)
    return array_of_articles





url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5'
array_of_articles = get_article_data(url) # request to arxiv


# it goes through the links and get data from database
for article in array_of_articles:
    pdf_url = article['pdf_link']
    text = send_a_pdf_to_api_and_get_text_from_api(pdf_url)
    print(text[:80])

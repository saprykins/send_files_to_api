import requests


def get_text_from_api(file_url):

    # it's the internal api 
    # is used to send pdf-file and get document_id
    post_url = "http://localhost:5000/documents"

    files = {"file": open(file_url, "rb")}

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

print(get_text_from_api('sample.pdf'))

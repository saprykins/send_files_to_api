import requests

# we can check w/ this api
# test_url = "http://httpbin.org/post"

# it's my api
# is used to send pdf-file and get document_id
post_url = "http://localhost:5000/documents"

files = {"file": open("sample.pdf", "rb")}

# send file
response = requests.post(post_url, files=files)

# get id of the document saved in database
document_id = response.json()['id']

test_get = "http://localhost:5000/text/"+str(document_id)+".txt"

# get data
# payload = {'id': '55'}
response = requests.get(test_get)
# print(response.text['text'])
dict = response.json()
print(dict['text'])




"""
test_file = open("sample.pdf", "rb")
test_response = requests.post(test_url, files = {"form_field_name": test_file})
print(test_response)
"""


'''
if test_response.ok:
    print(test_response.text)
'''

'''
files = {
    'file': ('sample.pdf', open('sample.pdf', 'rb')),
}

files = {
    "file": open("sample.pdf", "rb"),
    # "file": open("sample_2.pdf", "rb"),
    # "file": open("sample_3.pdf", "rb"),
}
'''

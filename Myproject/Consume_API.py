import requests

print('API request test')
## To consume the API, you have to mantain the server running and then write the desired rest point as a aparameter for the requests.get() function
## News Articles list: http://127.0.0.1:8000/api/
## Categories list: http://127.0.0.1:8000/api/categories
## Authors list: http://127.0.0.1:8000/api/authors
 
response = requests.get('http://127.0.0.1:8000/api/categories')
print(response.json())
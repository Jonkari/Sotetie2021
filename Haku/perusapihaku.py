import requests

data = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(data.json())

print(data.json()['userId'])
print(type(data.json()))
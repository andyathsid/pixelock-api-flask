import requests

url = 'http://127.0.0.1:5000/api/encode'

data = {'image': 'https://github.com/andyathsid/parkinson-disease-hand-writing-detection-pytorch-lightning/blob/main/data/CombinedAll/parkinson/0002-1.jpg?raw=true',
        'message': 'Hello, world!'}

result = requests.post(url, json=data).json()
print(result)
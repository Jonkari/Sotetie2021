import requests
import json
data = requests.get('https://opintopolku.fi/lo/search?start=0&rows=25&lang=fi&searchType=LO&text=avoin%20yo', headers={"Caller-Id":"JokuStringivaa"})
print(data.json())
fo=open("data.json", "w")
fo.write(json.dumps(data.json(), indent=1, sort_keys=True))
fo.close()
print(type(data.json()))
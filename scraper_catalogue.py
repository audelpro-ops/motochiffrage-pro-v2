import requests

headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "fr-FR,fr;q=0.9"}

url = "https://www.pieces-yam.com/yamaha-moto/1000-MOTO/2020"
r = requests.get(url, headers=headers, timeout=10)
print("Status: " + str(r.status_code))
print("Taille: " + str(len(r.text)))
print(r.text[:3000])

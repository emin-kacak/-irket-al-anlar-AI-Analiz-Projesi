import requests

try:
    response = requests.post("http://localhost:5000/soru-sor", json={
        "soru": "Excel verisini yorumlar mısın?"
    })
    response.raise_for_status()
    print("Yapay Zeka'dan Gelen Cevap:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")

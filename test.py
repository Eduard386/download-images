import requests
import os
import time

def get_tor_session():
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    return session


session = get_tor_session()

for i in range(0, 5):
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    os.system("brew services restart tor")
    time.sleep(10)
    print(session.get("https://ident.me").text)

# Following prints your normal public IP
print(requests.get("https://ident.me").text)

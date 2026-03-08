
import requests, random, json
from concurrent.futures import ThreadPoolExecutor

PORT = 8090
TIMEOUT = 2
TARGET = 20

def random_ip():
    return ".".join(str(random.randint(1,255)) for _ in range(4))

def check(ip):
    try:
        r = requests.get(f"http://{ip}:{PORT}/echo", timeout=TIMEOUT)
        if r.status_code == 200:
            return f"{ip}:{PORT}"
    except:
        return None

ips = [random_ip() for _ in range(3000)]

working = []

with ThreadPoolExecutor(max_workers=200) as ex:
    results = ex.map(check, ips)

for r in results:
    if r:
        working.append(r)
    if len(working) >= TARGET:
        break

with open("servers.json","w") as f:
    json.dump(working,f)

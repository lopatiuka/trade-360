import requests
from multiprocessing.pool import ThreadPool
import datetime
from time import time as timer
import pycountry

urls = []
count = {'available': 0, 'unavailable': 0}
path_to_files = 'https://blockgain.org/img/flags%20(copy)'

for country in pycountry.countries:
    language = country.alpha_2
    filename = f'{language.lower()}.png'
    urls.append((filename, f'{path_to_files}/{filename}'))

def handle_response(url):
    path, url = url
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        count['available'] += 1
        with open(path, 'wb+') as f:
            f.write(response.content)
    elif response.status_code == 404:
        with open('404.txt', 'a+') as f:
            count['unavailable'] += 1
            f.write(f'[{datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")}] "{path}" Not Found.\n')

    return f'[{response.status_code}] "{path}"'


start = timer()
results = ThreadPool(8).imap_unordered(handle_response, urls)
for result in results:
    print(result)

print(f"Flags download finished after: {timer() - start}")
print(f"Download result: Available: {count['available']}, Unavailable: {count['unavailable']}")

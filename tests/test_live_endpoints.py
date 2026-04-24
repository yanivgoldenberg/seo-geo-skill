import requests
urls = ['https://yanivgoldenberg.com/llms.txt', 'https://yanivgoldenberg.com/favicon.ico']
for u in urls:
    try:
        r = requests.get(u, timeout=10)
        print(u, r.status_code)
        assert r.status_code == 200
    except Exception as e:
        print(u, 'FAIL', e)

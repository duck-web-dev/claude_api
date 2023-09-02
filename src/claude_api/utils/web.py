import requests
from curl_cffi import requests as requests_fake
from random import randint
import json

session = requests_fake.Session(impersonate="chrome107")
session.headers = {
    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.{randint(0, 9999)}.{randint(0, 9999)} Safari/537.36 Edg/114.0.1823.79",
}
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'application/json',
	'Origin': 'https://claude.ai',
	'Referer': 'https://claude.ai/chats',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-origin',
	'Connection': 'keep-alive'
}


def handle_response(response: requests.Response):
	if not response.ok:
		raise RuntimeError(f"Get request code {response.status_code}: '{response.text}'")
	try:
		return response.json()
	except:
		return response.text


def make_get_request(url: str, _cookie: str = '', _headers: 'dict[str, str]' = headers) -> 'dict | str':
	h = {}
	h.update(_headers)
	h['Cookie'] = _cookie
	response = requests.get(url, headers=h)
	return handle_response(response)
def make_delete_request(url: str, _cookie: str = '', data: str = '', _headers: 'dict[str, str]' = headers) -> 'dict | str':
	h = {}
	h.update(_headers)
	h['Cookie'] = _cookie
	response = requests.delete(url, data=(data or None), headers=h)
	return handle_response(response)

def make_post_request(url: str, data: dict, _cookie: str = '', _headers: 'dict[str, str]' = headers) -> 'dict | str':
	h = {}
	h.update(_headers)
	h['Cookie'] = _cookie
	# data = json.dumps(data)
	response = requests.post(url, json=data, headers=h, timeout=500)
	return handle_response(response)
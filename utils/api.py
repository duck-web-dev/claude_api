from random import randint
from typing import Literal
from utils.funcs import join_url
from utils.web import make_delete_request, make_get_request, make_post_request, handle_response
from utils.funcs import make_uuid
import json
from curl_cffi import requests as requests_fake

### Main
base_url = "https://claude.ai/api"
def make_api_call(path: str, api_key: str, method: Literal['POST', 'GET', 'DELETE'] = 'GET', data: 'dict | str' = {}, headers: dict = {}) -> 'str | list | dict':
	url = join_url(base_url, path)
	cookie = f"sessionKey={api_key}"
	if method == 'GET':
		res = make_get_request(url, cookie)
	elif method == 'POST':
		if headers:
			res = make_post_request(url, data, cookie, headers)
		else:
			res = make_post_request(url, data, cookie)
	elif method == 'DELETE':
		res = make_delete_request(url, data=(data or None), _cookie = cookie)
	return res


### Organizations
def get_organizations(api_key: str) -> 'list[dict]':
	return make_api_call('/organizations', api_key)


### Chats
def create_chat(org_id: str, name: 'str | None', api_key: str) -> str:
	''' Create chat and return its id '''
	chat_id = make_uuid()
	data = {
		'name': f"ClaudeClient_{name if name else chat_id[:4]}",
		'uuid': chat_id
	}
	return make_api_call(
		f'/organizations/{org_id}/chat_conversations',
		api_key, method = 'POST',
		data = data
	)
def delete_chat(org_id: str, chat_id: str, api_key: str):
	return make_api_call(
		f'/organizations/{org_id}/chat_conversations/{chat_id}',
		api_key,  method = 'DELETE',
		data = chat_id
	)
def get_chat(org_id: str, chat_id: str, api_key: str) -> dict:
	return make_api_call(
		f'/organizations/{org_id}/chat_conversations/{chat_id}',
		api_key
	)
def list_chats(org_id: str, api_key: str) -> 'list[dict]':
	''' List chats for given organization '''
	return make_api_call(f'/organizations/{org_id}/chat_conversations', api_key)


### Messages
def send_message(org_id: str, chat_id: str, text: str, api_key: str):
	# Really hard to bypass 403, nothing I can do to make code better :D
	session = requests_fake.Session(impersonate="chrome107")
	session.headers = {
		"User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.{randint(0, 9999)}.{randint(0, 9999)} Safari/537.36 Edg/114.0.1823.79"
	}
	res = session.request(
		url = join_url(base_url, '/append_message'),
		method = 'POST',
		json = {
			"completion": {
				"prompt": text,
				"timezone": "Europe/Moscow",
				"model": "claude-2"
			},
			"organization_uuid": org_id,
			"conversation_uuid": chat_id,
			"text": text,
			"stream": False,
			"attachments": []
		},
		headers = {
			"Cookie": f"sessionKey={api_key}",
			"Referer": f"https://claude.ai/chat/{chat_id}"
		}
	)
	handle_response(res)  # Check for errors
	text = ''
	for line in res.text.split('\n\n'):
		if not line: continue
		s = line.replace('data: ', '').strip()
		data = json.loads(s)
		if 'error' in data:
			return f"ERROR! Please try again: {data['error']}"
		if data['stop_reason'] or data['stop']: break
		text += data['completion']
	return text.strip()
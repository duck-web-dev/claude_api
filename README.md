# 🤖 Claude Python Client

Delivers an easy way to interact with the free Claude AI API. 



## 💾 Installation

`pip install git+https://github.com/duck-web-dev/claude_api.git`



## 🤔 Usage

Use the api key from cookies.

`from claude_api import ClaudeClient`

`client = ClaudeClient(api_key="YOUR_API_KEY")`


### List chats

`chats = client.list_chats()`

Returns a list of chats.


### Get a chat

`chat = client.get_chat(chat_id="123")`

Returns a chat object (dict) for the given chat ID.


### Create a chat

`chat = client.create_chat(name="MyChat12345")`

Creates a new chat and returns the chat id.
Note: only set the name if you know what you are doing.


### Delete a chat 

`client.delete_chat(chat_id="123")`

Deletes the chat with the given ID.


### Send a message

`client.send_message(chat_id="123", text="Hello!") `

Sends a message to the chat with the given ID.
import logging
from . import api
from . import chat

logging.basicConfig()

class ClaudeClient:
	def __init__(self, api_key: str, log_level = logging.INFO):
		self.__api_key: str = api_key
		self.__organization_id = None
		self.logger = logging.getLogger()
		self.logger.level = log_level
		self.logger.info(f"Init {self.__class__.__name__} with key ****-{api_key[-4:]}")
	
	@property
	def organization_id(self) -> str:
		if self.__organization_id is None:
			self.logger.info("Getting organization id...")
			c = api.get_organizations(self.__api_key)
			self.__organization_id = c[0]['uuid']
			self.logger.info(f"  Organization id: {self.__organization_id}")
		return self.__organization_id

	def list_chats(self, only_client: bool = False):
		''' If `only_client` is True, returns only chats that were created using this client. '''
		self.logger.info(f"List chats: {'only client'if only_client else'all'}")
		r = api.list_chats(
			self.organization_id,
			self.__api_key
		)
		if only_client:
			r = list(filter(lambda o: 'ClaudeClient_' in o['name'], r))
		self.logger.info(f"  Found {len(r)} chats: {[x['name'] for x in r]}")
		return r

	def get_chat(self, chat_id: str):
		c = chat.Chat()
		messages = api.get_chat(
			self.organization_id,
			chat_id,
			self.__api_key
		)
		for msg in messages['chat_messages']:
			c.push(
				chat.Message(
					id=msg['uuid'],
					text=msg['text'],
					sender=msg['sender']
				)
			)
		return c

	def create_chat(self, name: str = None) -> str:
		self.logger.info(f"Creating chat with name '{name}' ...")
		chat_id = api.create_chat(self.organization_id, name, self.__api_key)
		self.logger.info(f"  Chat uuid: {chat_id}")
		return chat_id

	def delete_chat(self, chat_id: str):
		self.logger.info(f"Deleting chat {chat_id}")
		api.delete_chat(self.organization_id, chat_id, self.__api_key)

	def send_message(self, chat_id: str, text: str):
		self.logger.info(f"Sending '{text[:10]}...' to chat {chat_id} ...")
		res = api.send_message(
			self.organization_id,
			chat_id, text,
			self.__api_key,
		)
		self.logger.info(f"  Response: {res}")
		return res
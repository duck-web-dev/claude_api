from utils.funcs import make_uuid


class Message:
	def __init__(self, text: str, sender: str, id: str = ''):
		self.id: str = (id or make_uuid())
		self.text: str = text
		self.sender: str = sender

class Chat:
	def __init__(self):
		self.history: 'list[Message]' = []
	def push(self, msg: Message) -> None:
		self.history.append(Message)
	def __getitem__(self, key: 'str | int'):
		if isinstance(key) == int:
			try:
				return self.history[key]
			except IndexError:
				raise IndexError('Index out of range')
		else:
			c = tuple(map(lambda o: o.id == key, self.history))
			try:
				return c[0]
			except IndexError:
				raise IndexError(f'No message with id "{key}"')
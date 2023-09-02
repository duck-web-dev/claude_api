import uuid

def join_url(*s: str) -> str:
    return '/'.join(x.strip('/') for x in s)

def make_uuid() -> str:
    return str(uuid.uuid4())
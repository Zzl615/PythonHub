import time

import jwt


class MyJwt:

    def __init__(self, secret: str, ttl: int):
        self.secret = secret
        self.ttl = ttl

    def encode(self, payload: dict):
        return jwt.encode(payload=payload, key=self.secret, algorithm='HS256')

    def decode(self, token: str):
        return jwt.decode(jwt=token, key=self.secret, algorithms='HS256', verify_exp=True)

    def generate_user(self, user_id):
        return self.encode(payload={
            'id': user_id,
            'iss': 'lab_coat',
            'nbf': int(time.time()),
            'iat': int(time.time()),
            'exp': int(time.time()) + self.ttl,
        })

    def generate_admin(self, phone):
        return self.encode(payload={
            'id': phone,
            'iss': 'llm_doctor_tenant_admin',
            'nbf': int(time.time()),
            'iat': int(time.time()),
            'exp': int(time.time()) + self.ttl,
        })

if __name__ == '__main__':
    # object = MyJwt(secret='CWnXDX5y8i1MPa3', ttl=60*60*24*180)
    # token = object.generate_admin(18770813304)
    object = MyJwt(secret='K643aHGxxnzHqAf', ttl=60*60*24*180)
    token = object.generate_admin(17765151889)
    print(f'Bearer {token}')
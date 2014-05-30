from app import app
from flask import json


v = app.test_client()

t = dict()
t['uname'] = 'username'
t['pw'] = 'password'

ts = json.dumps(t)

c = app.test_request_context('/createUser', method='POST')

with c:
   r = v.post('/createUser', headers={'content-type':'application/json'}, data=ts)




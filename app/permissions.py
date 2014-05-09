from app import get_db
from database_utilities import query_db, DatabaseException
EMPLOYEE = 0b0001
ADMIN = 0b0011
BLOCKED_USER = 0b1000
PERMISSION_QUERY = 'select permissionLevel from Permissions where pid=? and qid=?'

def has_flag(uid, qid, necessary_permission):
    arguments = (uid, qid)
    rows = query_db(PERMISSION_QUERY, arguments)
    if not rows:
      return False
    elif len(rows) == 0:
      return False
    else:
      actual_permission = rows[0]['permissionLevel']
      return (necessary_permission & actual_permission) == necessary_permission

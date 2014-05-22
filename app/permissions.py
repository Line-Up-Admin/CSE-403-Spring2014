from app import get_db
from database_utilities import query_db, DatabaseException
EMPLOYEE = 0b0001
ADMIN = 0b0011
BLOCKED_USER = 0b1000
PERMISSION_QUERY = 'select permission_level from Permissions where pid=? and qid=?'
ADD_PERMISSION = 'insert into Permissions values(?, ?, ?)'

def has_flag(uid, qid, necessary_permission):
    arguments = (uid, qid)
    rows = query_db(PERMISSION_QUERY, arguments)
    if not rows:
      return False
    elif len(rows) == 0:
      return False
    else:
      actual_permission = rows[0]['permission_level']
      return (necessary_permission & actual_permission) == necessary_permission

def add_permission(pid, qid, permission):
    db = get_db()
    db.execute(ADD_PERMISSION, (pid, qid, permission))
    db.commit()

def add_permission_list(pids, qid, permission):
    db = get_db()
    for pid in pids:
        db.execute(ADD_PERMISSION, (pid, qid, permission))
    db.commit()

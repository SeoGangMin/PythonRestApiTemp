from database import init_db
init_db()

from database import db_session
from models import User

u = User('admin', 'admin@localhost')
db_session.add(u)
db_session.commit()

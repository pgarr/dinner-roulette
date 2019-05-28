from app import create_app, db
from app.models import User
from tests.base_test import TestConfig

app = create_app(TestConfig)
db.session.remove()
db.drop_all()
db.create_all()

# users test test2 admin
user = User(username="test", email="test@test.com")
user.set_password("test")
db.session.add(user)
user2 = User(username="test2", email="test2@test.com")
user2.set_password("test")
db.session.add(user2)
admin = User(username="admin", email="admin@test.com", admin=True)
admin.set_password("admin")
db.session.add(admin)

db.session.commit()

app.run(port=5000, debug=False)

from playhouse.db_url import connect
from peewee import Model
from peewee import IntegerField
from peewee import CharField
from peewee import BooleanField
from flask_login import UserMixin


db = connect("sqlite:///peewee_db.sqlite")

if not db.connect():
    print("接続NG")
    exit()
print("接続OK")


class User(UserMixin, Model):

    id = IntegerField(primary_key=True)
    name = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = "user"


class LineUser(Model):
    id = IntegerField(primary_key=True)
    line_id = CharField()
    prefecture = CharField()
    municipality = CharField()

    class Meta:
        database = db
        table_name = "line_user"


class LineUserInterest(Model):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    category01 = BooleanField(null=True)
    category02 = BooleanField(null=True)
    category03 = BooleanField(null=True)

    class Meta:
        database = db
        table_name = "line_user_interest"


db.drop_tables([User, LineUser, LineUserInterest])
db.create_tables([User, LineUser, LineUserInterest])

from playhouse.db_url import connect
from peewee import Model
from peewee import IntegerField
from peewee import CharField
from peewee import BooleanField


db = connect("sqlite:///peewee_db.sqlite")

if not db.connect():
    print("接続NG")
    exit()
print("接続OK")


class User(Model):
    id = IntegerField(primary_key=True)
    line_id = CharField()
    prefecture = CharField()
    municipality = CharField()

    class Meta:
        database = db
        table_name = "user"


class UserInterest(Model):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    category01 = BooleanField(null=True)
    category02 = BooleanField(null=True)
    category03 = BooleanField(null=True)

    class Meta:
        database = db
        table_name = "user_interest"


# db.drop_tables([User, UserInterest])
db.create_tables([User, UserInterest])

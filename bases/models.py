from peewee import *


db = SqliteDatabase(r'bases\database.db')


class BaseModel(Model):
    class Meta:
        database = db
        

class User(BaseModel):
    user_id = IntegerField()
    user_name = CharField(max_length=50)
    data = TextField()
    search_param = TextField()
    favourites = TextField()
    watched_movies = TextField()
    history = TextField()
    
    
db.create_tables([User])

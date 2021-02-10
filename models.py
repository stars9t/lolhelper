from peewee import (
    Model,
    CharField,
    TextField,
    SqliteDatabase
)

from config import DATABASE


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DATABASE)


class ChampionLink(BaseModel):
    """
    Model with russian_name and
    link format name for champion
    """
    russian_name = TextField()
    link = TextField()


class Champion(BaseModel):
    """
    Model with all info about champion(cache).
    """
    name = CharField(unique=True)
    roles = TextField()
    core_weapons = TextField()
    late_weapons = TextField()
    strong_against = TextField()
    weak_against = TextField()
    core_runes_branch = CharField()
    extra_runes_branch = CharField()
    core_runes = TextField()
    extra_runes = TextField()
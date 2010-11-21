from sqlalchemy import Table, Column, String, Integer, Text
from sqlalchemy.orm import mapper

sources = Table('sources',
                 Column('id', Integer, primary_key=True),
                 Column('name', String(100)),
                 Column('url', Text))

class Source(object):
    pass

mapper(sources, Source)
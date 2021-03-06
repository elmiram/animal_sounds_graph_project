# coding=utf-8
__author__ = 'elmira'

import sqlite3 as sqlite
import codecs

f = codecs.open('/home/elmira/zvukimu/zvukimu/static/colors.txt', 'r', 'utf-8') # todo change name!
# f = codecs.open('./static/colors.txt', 'r', 'utf-8') # todo change name!
colors = [i.rstrip() for i in f.readlines()]
f.close()

f = codecs.open('/home/elmira/zvukimu/zvukimu/static/lang_color.txt', 'r', 'utf-8') # todo change name!
# f = codecs.open('./static/lang_color.txt', 'r', 'utf-8') # todo change name!
lang_colors = {i.rstrip().split('\t')[0]: i.rstrip().split('\t')[1] for i in f.readlines()}
f.close()

class Concatenate:
    def __init__(self):
        self.str = []

    def step(self, value):
        # print value
        if value is not None:
            self.str.append(value)

    def finalize(self):
        return ', '.join(self.str)


class SQLClient(object):

    def __init__(self, db_file):
        self._connection = sqlite.connect(db_file)
        self._connection.create_aggregate("concat", 1, Concatenate)
        self._cursor = self._connection.cursor()
        self.__data = ''

    def insert(self, table, *args):
        query = self.__make_query(table, args)
        self._cursor.execute(query)
        self._connection.commit()

    def __make_query(self, table, args):
        try:
            q = u"INSERT into " + table + u" VALUES(" + u", ".join(str(i) for i in args) + u');'
            return q
        except:
            print table
            for i in args: print i

    def query(self, sql):
        self._cursor.execute(sql)
        m = self._cursor.fetchall()
        return m


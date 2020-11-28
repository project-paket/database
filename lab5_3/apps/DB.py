import psycopg2
from psycopg2 import sql
import os
import time


def crt_brack_on_start():
    myCmd = 'sh lab5_3/apps/dump.sh'
    os.system(myCmd)


def restore_db(name):
    print(name)
    myCmd = 'sh lab5_3/apps/restore.sh lab5_3/apps/dumps/{}'.format(name)
    print(myCmd)
    os.system(myCmd)



def watch_dir():
    res = []

    for i in sorted(os.listdir('lab5_3/apps/dumps')):
        tmp = time.ctime(os.path.getctime('lab5_3/apps/dumps/{}'.format(i))).split()
        res.append([i, '{}/{}/{}{}'.format(tmp[2], tmp[1], tmp[4], tmp[3])])

    return res


class DB():
    def __init__(self, login, password):
        try:
            self.conn = psycopg2.connect(dbname='elevatorr', user='user_1',
                                         password='password', host='188.225.76.56')
            self.conn.autocommit = True

            self.login = None
            self.lvl = None

            with self.conn.cursor() as cursor:
                columns = ('id', 'login', 'password', 'name_position')
                stmt = sql.SQL('SELECT {} FROM {}').format(
                    sql.SQL(',').join(map(sql.Identifier, columns)),
                    sql.Identifier('employee')
                )
                cursor.execute(stmt)
                for row in cursor:
                    if login.lower() == row[1] and password.lower() == row[2] and 'лаборант' == row[3].lower():
                        self.login = login.lower()
                        self.lvl = 0

                    elif login.lower() == row[1] and password.lower() == row[2] and 'бухгалтер' == row[3].lower():
                        self.login = login.lower()
                        self.lvl = 1

                    elif login.lower() == row[1] and password.lower() == row[2] and 'диспетчер' == row[3].lower():
                        self.login = login.lower()
                        self.lvl = 2

                    elif login.lower() == row[1] and password.lower() == row[2] and 'директор' == row[3].lower():
                        self.login = login.lower()
                        self.lvl = 3

                if not self.login:
                    self.conn = None
        except:
            self.restore('a')

    def restore(self, name):
        # name = 'dumps/db_2020-04-19:13:48:31.dump'
        myCmd = 'sh restore.sh {}'.format(name)

        #myCmd = 'sh lab5_3/apps/restore.sh lab5_3/apps/dumps/{}'.format(name)
        os.system(myCmd)

    def rollback(self):
        with self.conn.cursor() as cursor:
            cursor.execute('rollback;')

    def beautiful_change(self, mass):
        new_mass = []
        for i in mass:
            new_mass.append(i[0])
        return new_mass

    def con(self, new_mass, mass_table):
        beautiful_mass = []
        for i in range(mass_table.__len__()):
            beautiful_mass.append([])
            for j in range(len(mass_table[i])):
                beautiful_mass[i].append([new_mass[j], mass_table[i][j]])
        return beautiful_mass

    def create_nice_search(self, titles, args):
        string = "cast({} AS VARCHAR) LIKE '%{}%'".format(titles[0], args[0])
        for i in range(1, len(titles)):
            if args[i]:
                string = "{} AND  cast({} AS VARCHAR) LIKE '%{}%'".format(string, titles[i], args[i])

        return string

    def get_tables_all(self):
        with self.conn.cursor() as cursor:
            stmt = sql.SQL("SELECT table_name FROM information_schema.tables"
                           " WHERE table_schema NOT IN ('information_schema','pg_catalog');")

            cursor.execute(stmt)
            return self.beautiful_change(cursor.fetchall())

    def get_tables(self):
        if self.lvl == 3:
            with self.conn.cursor() as cursor:
                stmt = sql.SQL("SELECT table_name FROM information_schema.tables"
                               " WHERE table_schema NOT IN ('information_schema','pg_catalog') AND "
                               "table_name NOT LIKE '%_old';")

                cursor.execute(stmt)
                return self.beautiful_change(cursor.fetchall())

        if self.lvl == 0:
            return ['waybill', 'gost', 'stock', 'organization', 'laboratory_analysis']

        if self.lvl == 2:
            return ['waybill', 'stock', 'delivery']

        if self.lvl == 1:
            return ['waybill', 'person', 'employee', 'organization', 'laboratory_analysis']

    def output_titles(self, table):
        with self.conn.cursor() as cursor:
            stmt = sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = '{}';".format(table))
            cursor.execute(stmt)

            return self.beautiful_change(cursor.fetchall())

    def output_tables(self, table):
        if self.lvl == 0 and table == 'basket':
            with self.conn.cursor() as cursor:
                stmt = sql.SQL(
                    "SELECT * FROM waybill WHERE id = {};".format(self.get_need_user()[0][0]))
                cursor.execute(stmt)

                return self.con(self.output_titles(table), cursor.fetchall())
        with self.conn.cursor() as cursor:
            stmt = sql.SQL('SELECT * FROM {};'.format(table))
            cursor.execute(stmt)

            return self.con(self.output_titles(table), cursor.fetchall())


    def update(self, mass, table):
        with self.conn.cursor() as cursor:
            stmt = self.crt_update(mass, table)

            cursor.execute(stmt)

    def del_string(self, old, table):
        with self.conn.cursor() as cursor:
            stmt = "DELETE FROM {} WHERE id = {} ;".format(table, old)

            cursor.execute(stmt)

    def get_need_user(self):
        with self.conn.cursor() as cursor:
            stmt = sql.SQL('SELECT id FROM employee WHERE login=\'{}\';'.format(self.login))
            cursor.execute(stmt)

            return cursor.fetchall()

    def insert(self, mass, table):
        if self.lvl == 0:
            id_ = self.get_need_user()[0][0]
            mass[3] = str(id_)
        with self.conn.cursor() as cursor:
            stmt = self.crt_insert(mass, table)

            print(stmt)

            cursor.execute(stmt)

    def search_component(self, table, args):
        prov = False
        for i in args:
            if a != '':
                prov = True

        with self.conn.cursor() as cursor:
            stmt = sql.SQL('SELECT * FROM {} WHERE {};'.format(table,
                                                               self.create_nice_search(args=args,
                                                                                       titles=self.output_titles(table)
                                                                                       )
                                                               ))
            if prov:
                cursor.execute(stmt)
                return self.con(self.output_titles(table), cursor.fetchall())
            else:
                return self.output_tables(table)

    def change_to_norm_none(self, arg):
        if arg.lower() == 'none' or arg.lower() == 'null' or arg == '':
            return 'null'
        else:
            try:
                return int(arg)
            except:
                return "'{}'".format(arg)

    def crt_update(self, mass, table):
        args = self.output_titles(table)
        string = 'UPDATE {} SET {} = {}'.format(table, args[0], mass[0])
        for i in range(1, len(args)):
            string += ', {} = {}'.format(args[i], self.change_to_norm_none(mass[i]))
        string += ' WHERE id={};'.format(mass[-1])

        return string

    def crt_insert(self, mass, table):
        args = self.output_titles(table)
        string = 'INSERT INTO {} VALUES ('.format(table, args[0], mass[0])
        for i in range(len(args) - 1):
            string = '{} {},'.format(string, self.change_to_norm_none(mass[i]))

        string = '{} {});'.format(string, self.change_to_norm_none(mass[i+1]))

        return string

    def back_num(self, num, table):
        with self.conn.cursor() as cursor:
            args = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}_old' AND COLUMN_NAME NOT IN ('date_operation')".format(table)
            cursor.execute(args)
            args = self.beautiful_change(cursor.fetchall())
            string = "{}".format(args[0])
            for i in args[1:]:
                string += ', ' + i
            stmt = "SELECT {} FROM {}_old ORDER BY date_operation DESC LIMIT {};".format(string, table, num)
            cursor.execute(stmt)
            for i in cursor.fetchall():
                if i[-1] == 'INSERT':
                    self.del_string(i[0], table)
                elif i[-1] == 'DELETE':
                    mass = []
                    for j in i[:-1]:
                        mass.append(str(j))
                    self.insert(mass, table)
                elif i[-1] == 'UPDATE':
                    mass = []
                    for j in i[:-1]:
                        mass.append(str(j))
                    self.update(mass + [i[0]], table)

            print(cursor.fetchall())


#crt_brack_on_start()

a = DB('a', 'a')
scripts = None
link = 'waybill'
if __name__ == '__main__':
    a = DB('admin', 'admin')
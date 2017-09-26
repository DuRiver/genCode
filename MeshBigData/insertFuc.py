import psycopg2


# conn = psycopg2.connect(database="messdata", user="postgres", password="postgres", host="localhost", port="5432")

# cur = conn.cursor()


class SealedClassMeta(type):
    _types = set()

    def __init__(cls, name, bases, attrs):
        if cls._types & set(bases):
            raise(SyntaxError("Cannot inherit form a sealed class!"))
        cls._types.add(cls)


class pgsqlHelper(object):
    __metaclass__ = SealedClassMeta

    def __init__(self, database='meshdata', user='postgres', password='postgres', host='localhost', port='5432'):
        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        try:
            self._connPostSql = psycopg2.connect(
                database=self._database, user=self._user, password=self._password, host=self._host, port=self._port)
            self.conn = property(lambda self: self._connPostSql)
            self.cursor = self._connPostSql.cursor()
            print("Connect database successfully!")
        except psycopg2.Error as e:
            print('psycopg2 Error:{0}{1}'.format(e.args[0]))

    def closeConnection(self):
        if(self._connPostSql):
            self.cursor.close()
            self._connPostSql.close()
            print('The Connection is closed!')
        else:
            print('The connection is not open!')

    def executeNonQurery(self, sqlStr, param=None):
        statusNum = -1
        try:
            if(param is None):
                self.cursor.execute(sqlStr)
                self._connPostSql.commit()
                statusNum = 0
            else:
                self.cursor.execute(sqlStr, param)
                self._connPostSql.commit()
                statusNum = 0
            print("Query OK!")
            print('The Connection is not closed!!!')
        except psycopg2.Error as e:
            print('psycopg2 Error:{0}'.format(e.args[0]))
            print('Execute wrong!')
            print('The Connection is not closed!!!')
        return statusNum

    def executeScalar(self, sqlStr, param=None):

        try:
            if(param is None):
                self.cursor.execute(sqlStr)
                self._connPostSql.commit()
            else:
                sqlStrr = self.cursor.mogrify(sqlStr, param)
                self.cursor.execute(sqlStrr)
                self._connPostSql.commit()
            print("Query OK!")
            print('The Connection is not closed!!!')
        except psycopg2.Error as e:
            print('psycopg2 Error:{0}{1}'.format(e.args[0]))
            print('Execute wrong!')
            print('The Connection is not closed!!!')
        return self.cursor.fetchall()

# cur.copy_from(f, 'test', columns=('num', 'data'))
    def copy_from(self, file, table, sep='\t', columns=None):
        try:
            if columns is None:
                print('Wrong columns given!')
                return
            else:
                self.cursor.copy_from(file, table, columns=columns)
                print("copy successful!")
                print('The Connection is not closed!!!')
        except psycopg2.Error as e:
            print('psycopg2 Error:{0}{1}'.format(e.args[0]))
            print('Execute wrong!')
            print('The Connection is not closed!!!')
            


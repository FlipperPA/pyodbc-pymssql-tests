import pymssql, pyodbc, unittest
import time
import functools
import hashlib

def timethis(fn):
    """ Using the built-in time.time may be a naive approach, but the initial results look potentially useful. """

    @functools.wraps(fn)
    def dectimer(*args, **kwargs):
        begin = time.time()
        fn(*args, **kwargs)
        end = time.time() - begin
        timereport = fn.__name__ + ' executed in %f ms. ' % end

        if fn.__doc__ != None:
            print('Function description: ' + fn.__doc__)

        print(timereport + '\n')
        
        return
    return dectimer
    
def db_connect(db):
    if db == 'pymssql':
        conn = pymssql.connect(
            server="mydb.myserver.com",
            port=1433,
            user="pytest_user",
            password="",
            database="pytest")

        conn.autocommit(True)
        return conn
    elif db == 'pyodbc':
        cnx_str = 'DRIVER={FreeTDS};SERVER=mydb.myserver.com;PORT=1433;DATABASE=pytest;UID=pytest_user;PWD=;TDS_Version=7.3;'
        conn = pyodbc.connect(cnx_str, autocommit=True)
        return conn


@timethis
def test_table_create(cursor):
    """ Create table Python_Test """

    sql = ("IF OBJECT_ID('dbo.Python_Test', 'U') IS NOT NULL DROP TABLE dbo.Python_Test")
    cursor.execute(sql)
    sql = ("CREATE TABLE Python_Test (id INT IDENTITY (1, 1), unicode_test NVARCHAR(MAX))")
    cursor.execute(sql)


@timethis
def test_select_Python_Test_count(cursor):
    """ Determine whether table Python_Test exists in the database """

    sql = ("SELECT COUNT(*) AS result FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Python_Test'")
    cursor.execute(sql)

    for row in cursor:
        if row[0] != 1:
            raise Exception('Could not select table from database.')


@timethis
def test_insert_row(cursor, db):
    """ Test inserting rows into the database and returning the value of the IDENTITY column. """

    for x in range(1, 5000):
        md5 = str(hashlib.md5())

        if db == 'pymssql':
            sql = ("INSERT INTO Python_Test (unicode_test) OUTPUT INSERTED.id VALUES ('?')")
        else:
            sql = ("INSERT INTO Python_Test (unicode_test) OUTPUT INSERTED.id VALUES (?)")

        insert_id = cursor.execute(sql, md5)

        for row in cursor:
            if(x % 500 == 0):
                print('Inserted 500 rows, IDENTITY VALUE: %s' % (row[0],))


@timethis
def test_select_all_rows(cursor):
    """ SELECT all rows in table Python_Test """

    sql = ("SELECT * FROM Python_Test")
    cursor.execute(sql)

    for row in cursor:
        pass


@timethis
def test_select_rows_like(cursor):
    """ SELECT rows LIKE in table Python_Test """

    sql = ("SELECT * FROM Python_Test WHERE unicode_test LIKE 'a%'")
    cursor.execute(sql)

    for row in cursor:
        pass


@timethis
def test_create_stored_procedure(cursor):
    sql = """
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_NULLS OFF
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[usp_get_python_test]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[usp_get_python_test]
GO

CREATE PROCEDURE dbo.usp_get_python_test (
   @id INTEGER = 0,
   @unicode_test VARCHAR(32) OUTPUT
)
AS
BEGIN
    SELECT @unicode_test = unicode_test
    FROM Python_Test
    WHERE (id = @id) 
END
GO
SET QUOTED_IDENTIFIER OFF
GO
SET ANSI_NULLS ON
GO

GRANT EXECUTE ON [dbo].[usp_get_python_test]  to [pytest_user]
GO
"""


@timethis
def test_table_drop(cursor):
    sql = ("DROP TABLE Python_Test")
    cursor.execute(sql)

def test_implementation(db):
    print('Running tests via the ' + db + ' module.')
    print('------------------------------------------')
    test_dbs = ['pymssql', 'pyodbc']

    if db in test_dbs:
        run_tests(db)
    else:
        raise Exception('Specified database is not a valid option.')

def run_tests(db):
    conn = db_connect(db)
    cursor = conn.cursor()

    # Make sure to include each task to be tested
    test_table_create(cursor)
    test_select_Python_Test_count(cursor)
    test_insert_row(cursor, db)
    test_select_all_rows(cursor)
    test_select_rows_like(cursor)
    test_table_drop(cursor)

if __name__ == '__main__':
    test_implementation('pymssql')
    test_implementation('pyodbc')

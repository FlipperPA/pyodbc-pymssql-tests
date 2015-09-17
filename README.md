# pyodbc vs pymssql Performance Test

To test the performance of the Python modules against SQL Server, we wrote this simple test script. It connects to the same instance and same database (preferably). We've found pymssql to be more performant in our tests. To run:

* Spin up a virtualenv
* `pip install -r requirements.txt`
* python test_pyodbc_pymssql.py

## Example Output:

    Running tests via the pymssql module.
    ------------------------------------------
    Function description:  Create table Python_Test
    test_table_create executed in 0.314193 ms.

    Function description:  Determine whether table Python_Test exists in the database
    test_select_Python_Test_count executed in 0.008826 ms.

    Inserted 500 rows, IDENTITY VALUE: 500
    Inserted 500 rows, IDENTITY VALUE: 1000
    Inserted 500 rows, IDENTITY VALUE: 1500
    Inserted 500 rows, IDENTITY VALUE: 2000
    Inserted 500 rows, IDENTITY VALUE: 2500
    Inserted 500 rows, IDENTITY VALUE: 3000
    Inserted 500 rows, IDENTITY VALUE: 3500
    Inserted 500 rows, IDENTITY VALUE: 4000
    Inserted 500 rows, IDENTITY VALUE: 4500
    Function description:  Test inserting rows into the database and returning the value of the IDENTITY column.
    test_insert_row executed in 21.448038 ms.

    Function description:  SELECT all rows in table Python_Test
    test_select_all_rows executed in 0.051795 ms.

    Function description:  SELECT rows LIKE in table Python_Test
    test_select_rows_like executed in 0.029074 ms.

    test_table_drop executed in 0.004561 ms.

    Running tests via the pyodbc module.
    ------------------------------------------
    Function description:  Create table Python_Test
    test_table_create executed in 0.006053 ms.

    Function description:  Determine whether table Python_Test exists in the database
    test_select_Python_Test_count executed in 0.002657 ms.

    Inserted 500 rows, IDENTITY VALUE: 500
    Inserted 500 rows, IDENTITY VALUE: 1000
    Inserted 500 rows, IDENTITY VALUE: 1500
    Inserted 500 rows, IDENTITY VALUE: 2000
    Inserted 500 rows, IDENTITY VALUE: 2500
    Inserted 500 rows, IDENTITY VALUE: 3000
    Inserted 500 rows, IDENTITY VALUE: 3500
    Inserted 500 rows, IDENTITY VALUE: 4000
    Inserted 500 rows, IDENTITY VALUE: 4500
    Function description:  Test inserting rows into the database and returning the value of the IDENTITY column.
    test_insert_row executed in 34.694215 ms.

    Function description:  SELECT all rows in table Python_Test
    test_select_all_rows executed in 0.123788 ms.

    Function description:  SELECT rows LIKE in table Python_Test
    test_select_rows_like executed in 0.033885 ms.

    test_table_drop executed in 0.004684 ms.

## Credits:
* Timothy Allen
* Joseph Dougherty

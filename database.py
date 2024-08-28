import pyodbc


def append_table(server, database, trusted_conn, table_name, dataframe):
    # Set up the connection string
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_conn};TrustServerCertificate=yes;'

    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()

    # Generate the SQL insert statement dynamically
    columns = ", ".join(dataframe.columns)
    placeholders = ", ".join(["?"] * len(dataframe.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Insert DataFrame into SQL Server
    for index, row in dataframe.iterrows():
        cursor.execute(insert_query, tuple(row))

    cnxn.commit()
    cursor.close()
import sqlite3


def check_table(table_name: str,
                table_columns_conf: list[(str, str)],
                cursor: sqlite3.Cursor):
    # Check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    table_exists = cursor.fetchone()

    if not table_exists:
        # Create the table if it doesn't exist
        table_creation_query = f'''
                CREATE TABLE {table_name} (
                    {','.join([f'{col_name} {col_type}' for col_name, col_type in table_columns_conf])}
                );
            '''
        cursor.execute(table_creation_query)
        print(f'Table "{table_name}" created.')


def save_data(table_name: str,
              new_data_conf: list[(str, type)],
              cursor: sqlite3.Cursor):
    insert_query = f'''
        INSERT INTO {table_name} ({', '.join([col_name for col_name, _ in new_data_conf])})
        VALUES ({', '.join([f"'{col_data}'" for _, col_data in new_data_conf])});
    '''
    cursor.execute(insert_query)
    print(f'Executed query: {insert_query}')

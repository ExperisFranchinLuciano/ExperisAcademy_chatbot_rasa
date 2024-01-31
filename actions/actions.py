# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions/

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from database_connectivity import check_table, save_data


DB_NAME = 'recruiting_db'
USER_TABLE_NAME = 'user'
USER_COD_FISC_COLUMN = 'codice_fiscale'
USER_NAME_COLUMN = 'nome'


class RecognizeUserData(Action):

    def name(self):
        return 'recognize_user_data'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict[str, type],
            ) -> list[dict[str, type]]:
        # assigned to avoid UnboundLocalError
        db_name = DB_NAME
        if not db_name.split('.')[-1] == 'db':
            db_name += '.db'

        conn = sqlite3.connect(db_name)

        cod_fisc = tracker.get_slot('cod_fisc')
        print(cod_fisc)

        # Create a cursor object to interact with the database
        cursor: sqlite3.Cursor = conn.cursor()

        check_table(table_name=USER_TABLE_NAME,
                    cursor=cursor,
                    table_columns_conf=[(USER_COD_FISC_COLUMN, 'TEXT NOT NULL PRIMARY KEY'),
                                        (USER_NAME_COLUMN, 'TEXT NOT NULL')])

        sql_select_user = f'''
            SELECT {USER_COD_FISC_COLUMN}, {USER_NAME_COLUMN}
            FROM {USER_TABLE_NAME} 
            WHERE {USER_COD_FISC_COLUMN} = "{cod_fisc}"
        '''
        cursor.execute(sql_select_user)
        query_results = cursor.fetchall()

        # Checking if the user already exists, if not exists it will be added to database
        if not query_results:
            dispatcher.utter_message("Sei un nuovo utente, procediamo con l'inserimento dei dati!")
            first_name = tracker.get_slot('first_name')
            save_data(table_name=USER_TABLE_NAME,
                      new_data_conf=[(USER_COD_FISC_COLUMN, cod_fisc),
                                     (USER_NAME_COLUMN, first_name)],
                      cursor=cursor)
        else:
            first_name = query_results[1]

            dispatcher.utter_message(f"Ben ritrovato {first_name}!")
            return [SlotSet('first_name', first_name)]

        conn.commit()
        conn.close()
        return []

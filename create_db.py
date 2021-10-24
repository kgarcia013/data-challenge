import sqlite3
import pandas as pd

def sqlite_connection():
    conn = sqlite3.connect('support_data.db')
    c = conn.cursor()

    return c, conn

def import_csv_to_sqlite(conn, support_csv):
    support_df = pd.read_csv(support_csv)
    support_df.to_sql('support', conn, if_exists='append', index=False)

def main():

    c, conn = sqlite_connection()
    import_csv_to_sqlite(conn, 'ca_takehome_assessment.csv')

if __name__ == '__main__':
    main()
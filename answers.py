import csv
import pandas as pd
import sqlite3

def sqlite_connection():
    conn = sqlite3.connect('support_data.db')
    c = conn.cursor()

    return c, conn

def most_used_support_channel(conn):
    #Query to determine the used support channel
    SQL = """select SUPPORT_CHANNEL, COUNT(*) FROM support group by SUPPORT_CHANNEL ORDER BY count(*) desc"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())


def most_common_user_type(conn):
    # Query to determine the most common user type
    SQL = """select user_type, COUNT(*) FROM support group by user_type ORDER BY count(*) desc"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def country_with_most_support_tickets(conn):
    #Query to determine the country with the most support tickets
    SQL = """select COUNTRY, COUNT(*) FROM support group by COUNTRY ORDER BY count(*) desc"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def duration_data_gaps(conn):
    #CHAT_DURATION_MIN, FULL_RESOLUTION_TIME, CALL_LENGTH_MIN are all NULL or Blank

    #Support Channels where CHAT_DURATION_MIN, FULL_RESOLUTION_TIME, CALL_LENGTH_MIN  are null or blank
    SQL = """select SUPPORT_CHANNEL, count(*) from support where 
    CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and CALL_LENGTH_MIN is null group by SUPPORT_CHANNEL having count(*) > 0"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

    # User Types where CHAT_DURATION_MIN, FULL_RESOLUTION_TIME, CALL_LENGTH_MIN  are null or blank
    User_Type_SQL = """select user_type, count(*) from support where CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and 
    CALL_LENGTH_MIN is null group by user_type having count(*) > 0"""

    df = pd.read_sql_query(User_Type_SQL, conn)
    print(df.head())

    # Issue Types where CHAT_DURATION_MIN, FULL_RESOLUTION_TIME, CALL_LENGTH_MIN  are null or blank
    Issue_Types_SQL = """select ISSUE_TYPE_CATEGORY, count(*) from support where CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and 
    CALL_LENGTH_MIN is null group by user_type having count(*) > 0"""

    df = pd.read_sql_query(Issue_Types_SQL, conn)
    print(df.head())

def call_length_data_gaps(conn):
    #CALL_LENGTH_MIN column with negative numbers
    SQL = """select COUNT(*) from support where CALL_LENGTH_MIN < 0"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def user_type_data_gaps(conn):
    #Count of user types that are null
    SQL = """SELECT COUNT(*) from support  WHERE user_type is null"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def highest_survey_scores(conn):
    # Highest Average Survey Score by Category
    SQL = """select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY 
    HAVING AVG(SURVEY_SCORE) ORDER BY  AVG(SURVEY_SCORE) DESC"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def lowest_survey_scores(conn):
    #Lowest Average Survey Score by Category
    SQL = """select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY 
    HAVING AVG(SURVEY_SCORE) ORDER BY  AVG(SURVEY_SCORE) ASC"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def no_survey_scores(conn):
    #Categories with no Average Score -- No Survey Scores have been recorded
    SQL = """select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY HAVING AVG(SURVEY_SCORE) IS NULL"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())

def count_of_surveys_from_lowest_users(conn):

    #Gets the number opf survey responses from any issue type that has a response score below 4.0
    SQL = """select count(*) AS 'NO_SURVEY_SCORE', (select count(*) from support where ISSUE_TYPE_CATEGORY IN ('in development/sunset', 'business features and profile', 'hellosign api', 'passwords app', 'service and support') 
    and SURVEY_SCORE is not null) AS 'SURVEY_SCORE' from support where ISSUE_TYPE_CATEGORY IN
    ('in development/sunset', 'business features and profile', 'hellosign api', 'passwords app', 'service and support') and SURVEY_SCORE is null"""

    df = pd.read_sql_query(SQL, conn)
    print(df.head())


def main():

    c, conn = sqlite_connection()

    #PART 1
    most_used_support_channel(conn)
    most_common_user_type(conn)
    country_with_most_support_tickets(conn)

    #PART 2
    duration_data_gaps(conn)
    call_length_data_gaps(conn)
    user_type_data_gaps(conn)

    #PART 3
    highest_survey_scores(conn)
    lowest_survey_scores(conn)
    no_survey_scores(conn)
    count_of_surveys_from_lowest_users(conn)

if __name__ == '__main__':
    main()
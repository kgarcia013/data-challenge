
#### Below are the answers to my questions. Please note: All Queries  presented in this file and can also be viewed as dataframes in the following python file (answers.py). All SQL answers are written using SQLITE.

#### [Part 1 - Exploratory Analysis] Paint a picture of the support experience. What are the typical handle times by support channel? Are there differences between user types? Don’t worry about being exhaustive here, just pick a few interesting things to highlight.

1. SUPPORT_CHANNEL: it looks like the most used SUPPORT_CHANNEL's are **chat** and **email**
   1. Query as Follows: `select SUPPORT_CHANNEL, COUNT(*) FROM support group by SUPPORT_CHANNEL ORDER BY count(*) desc`
2. USER_TYPE: the most common user_types are **paid individual** and **business**
   1. Query as follows: `select user_type, COUNT(*) FROM support group by user_type ORDER BY count(*) desc`
3. COUNTRY: Most Support tickets come from the **us** and **other**. Are not all countries listed in the database?
   1. Query as follows: `select COUNTRY, COUNT(*) FROM support group by COUNTRY ORDER BY count(*) desc`

#### [Part 2 - Data] What data issues are you concerned about, if any? Is there additional data you’d like to see/collect?

##### Data Gaps

1. Scientific Notation: When I opened the file the first thing I noticed was the Scientific Notation in the CREATED_DAY and CLOSED_DAY columns. Because of this, we cannot accurately determine the average # of days a support case remains open. I would urge this get resolved immediately.

2. Duration Data Gaps:
   1. Another thing I noticed was that there are 364 records where the CHAT_DURATION_MIN, FULL_RESOLUTION_TIME, CALL_LENGTH_MIN are all NULL or Blank
     1. Below are some queries I wrote in SQLITE to get some more information on these 364 records. I thought it would be interesting to go ahead and grab the which SUPPORT_CHANNEL, user_type and ISSUE_TYPE_CATEGORY's correlate to this data gap.

        `select SUPPORT_CHANNEL, count(*) from support where CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and CALL_LENGTH_MIN is null group by SUPPORT_CHANNEL having count(*) > 0`

        `select user_type, count(*) from support where CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and CALL_LENGTH_MIN is null group by user_type having count(*) > 0`

        `select ISSUE_TYPE_CATEGORY, count(*) from support where CHAT_DURATION_MIN is NULL and FULL_RESOLUTION_TIME IS null and CALL_LENGTH_MIN is null group by user_type having count(*) > 0`
  2. I also noticed that the FULL_RESOLUTION_TIME does not  equal the CALL_LENGTH_MIN + CHAT_DURATION_MIN.

3.  CALL_LENGTH_MIN: Another data gap I noticed were that there were negative numbers in the CALL_LENGTH_MIN column. There were only 2, however this still raises some alarms of the validity of the rest of the information in the Column.
   1. Below is the Query I used to get this information:
      `select COUNT(*) from support where CALL_LENGTH_MIN < 0`

4. user_type: I also noticed that there were 363 records in where the user_type was not indicated in the support ticket. If the user_type is not in any of the categories listed in the csv file, I would reccomend an 'Other' option be added to remove the data gap.
      1. Below is the SQL query I used to get this information: `SELECT COUNT(*)from support  WHERE user_type is null`
5. CREATE_TIME: It looks like the CREATE_TIME is in Minutes:Seconds. I think this should be Hour:Minute:Seconds to get a better analysis of the exact time the support tickets are being recorded.

##### Additional Data

1. Additional User Information: Having additional user information would be very helpful in determining the current state of the support department and ways to improve. Information we could get if we had more user information include, which users have the largest support windows, get more refined details on the geographical information on these users, determine if there are enough employee coverage etc.
2. FULL_RESOLUTION_TIME: I want to see more information on the FULL_RESOLUTION_TIME column. I noticed in the data gaps that it does not equal the CHAT_DURATION_MIN +CALL_LENGTH_MIN. How does this get calculated?
3. Survey Score: I would be interested to see the different avenues, in which the survey was sent to the user (email, text, voice, etc.).Perhaps there are certain avenues that have a better response rate.

#### [Part 3 - Insights] What types of tickets tend to receive the best survey scores, or the worst? What suggestions do you have to improve the quality of the support experience?

#### Survey Score Results

1. Highest Survey Scores: The ISSUE_TYPE_CATEGORY with the highest scores are **teams** and **integrations**.
   1. Query used as follows: `select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY HAVING AVG(SURVEY_SCORE) ORDER BY  AVG(SURVEY_SCORE) DESC`
2. Lowest Survey Scores: The ISSUE_TYPE_CATEGORY WITH THE lowest score is in **development/sunset**
   1. Query used as follows: `select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY HAVING AVG(SURVEY_SCORE) ORDER BY  AVG(SURVEY_SCORE) ASC`
3. No Survey Scores Reported: The ISSUE_TYPE_CATEGORY that had no scores recorded are: **agent do not use**, **helloworks**, **privacy**, **salesforce**, **salesforce-apex**, **test super category**, and **unknown**
   1. Query used as follows: `select ISSUE_TYPE_CATEGORY, AVG(SURVEY_SCORE) from support GROUP BY ISSUE_TYPE_CATEGORY HAVING AVG(SURVEY_SCORE) IS NULL`

Suggestions:
1. I think it would be helpful to focus on the 7 categories are currently don't have any Survey Scores reported. I mentioned in the additional data section that it would be nice to have more information on the types of avenues surveys are being sent. Maybe this is an issue with not having enough ways users get these surveys. Its definitely worth looking into.
2. Looking the Average Survey Score's it looks like , 16/21 issue types have an Average rating  4.0 and above. However, taking a look at the categories, it looks like 3833 support tickets did not respond to the survey, skewing the results. In total, only 390 users send feedback. I think it would be helpful to bring the survey responses up and follow my suggestion in 1.
      1. Query used is as follows: `select count(*) AS 'NO_SURVEY_SCORE', (select count(*) from support where ISSUE_TYPE_CATEGORY IN ('in development/sunset', 'business features and profile', 'hellosign api', 'passwords app', 'service and support')
      and SURVEY_SCORE is not null)  AS 'SURVEY_SCORE'
      from support where ISSUE_TYPE_CATEGORY IN ('in development/sunset', 'business features and profile', 'hellosign api', 'passwords app', 'service and support') and SURVEY_SCORE is null`

For each question above, justify your answer. We care about the thought process that led to your answer more than the answer itself. Please include the answers to the prompts, as well as any code (Python, R, or whatever you worked with) that you used for the analysis.

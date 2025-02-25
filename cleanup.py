import sqlite3

from helpers import get_db_path, get_timeframes
from traceback import print_tb

timeframes = get_timeframes()

print(timeframes)

for timeframe in timeframes:
    with sqlite3.connect(get_db_path(timeframe)) as connection:
        try:
            c = connection.cursor()

            print("Cleanin up!")
            c.execute('BEGIN TRANSACTION')
            # Remove values that we don't want
            sql = "DELETE FROM parent_reply WHERE parent IS NULL OR parent == 'False' OR parent == '0'"
            c.execute(sql)
            connection.commit()
            # c.execute("VACUUM")
            # connection.commit()

            sql = "SELECT COUNT(comment_id) FROM parent_reply"
            c.execute(sql)
            result = c.fetchone()
            if result is not None:
                res = result[0]
                print(f'Cleanup done, paired rows: {res}')
        except Exception as e:
            print('Something broke')
            print(e)

print('Done')

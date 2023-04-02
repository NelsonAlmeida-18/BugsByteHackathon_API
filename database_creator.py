import sqlite3
import pandas as pd


def create_db():
    conn = sqlite3.connect('SmartMatch')

    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT, 
                [name] TEXT, 
                [email] TEXT,
                [contact] TEXT,
                [bio] TEXT,
                [pwd] TEXT,
                [dob] DATE,
                [academicArea] TEXT,
                [academicDegree] TEXT,
                [picture] BLOB,
                [user_interests] INTEGER,
                [location] TEXT,
                [user_preferences] INTEGER,
                FOREIGN KEY (user_interests) REFERENCES interests (id),
                FOREIGN KEY (user_preferences) REFERENCES preferences (id)
            );
            ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS interests
                ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [Mathematics] BOOLEAN,
                [Portuguese] BOOLEAN,
                [English] BOOLEAN,
                [German] BOOLEAN,
                [Physics] BOOLEAN,
                [Chemistry] BOOLEAN,
                [Economics] BOOLEAN,
                [Biology] BOOLEAN,
                [Geology] BOOLEAN,
                [History] BOOLEAN,
                [Computing] BOOLEAN,
                [Engineering] BOOLEAN,
                [Medicine] BOOLEAN,
                [Nursing] BOOLEAN,
                [Pharmacy] BOOLEAN,
                [Education] BOOLEAN,
                [Law] BOOLEAN,
                [Psychology] BOOLEAN,
                [Politics] BOOLEAN,
                [Sports] BOOLEAN
                );
                ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS place(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [street] TEXT,
                [city] TEXT,
                [country] TEXT,
                [studytype] TEXT,
                [rating] TEXT
                )''')
    

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [bph] INTEGER,
                [studylocal] TEXT,
                [music] BOOLEAN,
                [schedule] INTEGER,
                [talkative] BOOLEAN
                )''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS match(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [fromid] INTEGER,
                [toid] INTEGER,
                FOREIGN KEY (fromid) REFERENCES user (id),
                FOREIGN KEY (toid) REFERENCES user(id)
                )''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS swipe(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [userid] INTEGER,
                [targetid] INTEGER,
                [right] INTEGER,
                [left] INTEGER,
                FOREIGN KEY (userid) REFERENCES user (id),
                FOREIGN KEY (targetid) REFERENCES user (id)
                )''')

    conn.commit()

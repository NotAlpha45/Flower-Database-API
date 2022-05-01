import sqlite3

cursor = sqlite3.connect("flowers.db")

# cursor.execute(
#     '''
#     DROP TABLE Flowers
#     '''
# )
# cursor.commit()
# Creating a table

cursor.execute(
    '''
    CREATE TABLE Flowers (
        flower_id INTEGER PRIMARY KEY,
        genus TEXT,
        species TEXT,
        petal_count INTEGER,
        color TEXT
    );
    '''
)
cursor.commit()

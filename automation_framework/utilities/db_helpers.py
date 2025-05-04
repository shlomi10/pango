import sqlite3

class DatabaseHelper:
    def __init__(self, db_name="data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                 city TEXT PRIMARY KEY,
                 temperature REAL,
                 feels_like REAL,
                 avg_temp REAL
                 )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_history (
                 city TEXT,
                 temperature REAL,
                 feels_like REAL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                  )''')

    def insert_weather_data(self, city, temperature, feels_like):
        avg_temp = (temperature + feels_like) / 2
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO weather_data (city, temperature, feels_like, avg_temp)
                VALUES (?, ?, ?, ?)
            ''', (city, temperature, feels_like, avg_temp))

    def get_weather_data(self, city):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM weather_data WHERE city=?", (city,))
        return cursor.fetchone()

    def get_city_with_highest_avg_temp(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT city, MAX(avg_temp) FROM weather_data")
        return cursor.fetchone()

    def insert_weather_history(self, city, temperature, feels_like):
        with self.conn:
            self.conn.execute('''
                              INSERT INTO weather_history (city, temperature, feels_like)
                              VALUES (?, ?, ?)
                              ''', (city, temperature, feels_like))



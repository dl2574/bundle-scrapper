import sqlite3
import os
import logging

DB_PATH = "./"
DB_NAME = "bundle_db.sqlite3"

class DataManager():
    def _checkPathExistsOrCreate(self):
        if not os.path.exists(self.db_path):
            try:
                os.mkdir(self.db_path)
            except OSError as error:
                logging.error(f"Error creating db path: {error}")
                return 1
            
        return 0
    
    def _checkDbExists(self):
        if os.path.isfile(self.full_path):
            return True
        else:
            return False
    
    def connect(self, db_path=DB_PATH, db_name=DB_NAME):
        """Connects to the database. If one does not exist at the specified path
        then create one and connect

        Args:
            db_path (string, optional): The file path to the database location. Defaults to DB_PATH.
            db_name (string, optional): The name of the database. Defaults to DB_NAME.

        Returns:
            bool: bool representing if the connection was created successfully
        """
        self.db_path = db_path
        self.db_name = db_name
        self.full_path = os.path.join(self.db_path, self.db_name)
        self.conn = None
        
        # If there was an error return a empty connection
        if self._checkPathExistsOrCreate() == 1:
            return False
            
        if self._checkDbExists():
            self.conn = sqlite3.connect(self.full_path)
        else:
            self.conn = sqlite3.connect(self.full_path)
            self.conn.execute('''CREATE TABLE BUNDLES
                    (ID INT PRIMARY KEY,
                    TITLE VARCHAR(255) NOT NULL,
                    AUTHOR TEXT NOT NULL,
                    DESCRIPTION VARCHAR(255) NOT NULL,
                    URL VARCHAR(255) NOT NULL,
                    STAMP TEXT NOT NULL,
                    CATEGORY TEXT NOT NULL);''')
              
        return True
    
    def close(self):
        self.conn.close()
        
    def add_bundle(self, bundle):
        self.conn.execute("""INSERT INTO BUNDLES (TITLE,AUTHOR,DESCRIPTION,URL,STAMP,CATEGORY) 
                          VALUES (?,?,?,?,?,?);""",(bundle.title, bundle.author, bundle.description, bundle.url, bundle.stamp, bundle.category))
        self.conn.commit()
    
    def get_bundle_list_by_category(self, category):
        return self.conn.execute("""SELECT TITLE FROM BUNDLES WHERE CATEGORY = ?;""", [category])
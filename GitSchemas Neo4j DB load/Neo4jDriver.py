from dotenv import dotenv_values
from neo4j import GraphDatabase

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Access specific variables
db_host = env_vars.get("DB_HOST")
db_user = env_vars.get("DB_USER")
db_password = env_vars.get("DB_PASSWORD")
db_database = env_vars.get("DB_DATABASE")

class Neo4jDriver:
    def __init__(self, uri=db_host, username=db_user, password=db_password, database=db_database):
        self._uri = uri
        self._username = username
        self._password = password
        self._database = database
        self._driver = None

    def connect(self):
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._username, self._password), database=self._database)
            print("Connected to Neo4j database!")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def close(self):
        if self._driver is not None:
            self._driver.close()
            print("Connection to Neo4j closed.")
        else:
            print("No connection to close.")

    def execute_read_query(self, query, parameters=None):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return result.to_df()

    def execute_write_query(self, query, parameters=None):
        with self._driver.session() as session:
            result = session.write_transaction(self._write_transaction, query, parameters)
            try:
                return result.to_df()
            except:
                return None
            
    @staticmethod
    def _write_transaction(tx, query, parameters):
        result = tx.run(query, parameters)
        return result
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
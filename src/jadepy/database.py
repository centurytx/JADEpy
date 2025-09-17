import os
import pandas as pd
from dotenv import load_dotenv
from .utils import warning, debug
from sqlalchemy import create_engine, text

class Settings:
    DB_PASSWORD: str | None = None
    DB_PORT: str = "5432"
    DB_NAME: str = "production_DB_v2"
    DB_USER: str = "jadereader"
    AWS_PROFILE: str = "default"
    loaded_env = False


settings = Settings()

def load_env(repo_root: str = "") -> None:
    # Check the following locations for .env files:
    env_paths_to_try: list[str] = []
    home_dir = os.path.expanduser('~')
    if repo_root != "":
        env_paths_to_try.append(os.path.join(repo_root, '.env'))
    if home_dir:
        env_paths_to_try.append(os.path.join(home_dir, '.JADE.env'))
        env_paths_to_try.append(os.path.join(home_dir, '.env'))
    for env_path in env_paths_to_try:
        if os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path)
    settings.DB_PASSWORD = os.getenv('DB_READER_PASSWORD')
    env_port = os.getenv('DB_PORT')
    env_db_name = os.getenv('DB_DEFAULT_NAME')
    env_aws_profile = os.getenv('AWS_PROFILE')
    if env_db_name:
        settings.DB_NAME = env_db_name
    if not env_port is None:
        settings.DB_PORT = env_port
    if not env_aws_profile is None:
        settings.AWS_PROFILE = env_aws_profile

class Client:
    def __init__(self, db_name:str = "", db_url: str = "") -> None:
        """
        Initialize the client. The easiest way is to just specify the db_name, in which case it will look for
        the DB_READER_PASSWORD in the environment variable or a ~/.JADE.env file.
        Alternatively, you can specify the full db_url directly.
        Example db_url: 'postgresql://user:password@host:port/dbname'
        """
        if not settings.loaded_env:
            load_env()
            settings.loaded_env = True
        self.infer_db_url(db_name, db_url)
        debug(f"Connected to database")
        self.engine = create_engine(self.db_url)

    def infer_db_url(self, db_name, db_url) -> None:
        user = settings.DB_USER
        password = settings.DB_PASSWORD
        if not password:
            raise ValueError("DB_READER_PASSWORD environment variable or .env file with DB_READER_PASSWORD is required.")
        if db_name and db_url:
            raise ValueError("Specify either db_name or db_url, not both.")
        if db_url:
            self.db_url = db_url
            return
        # Allow db_name to override anything that's in POSTGRES_URL
        if db_name:
            self.db_url = f"postgresql://{user}:{password}@localhost:{settings.DB_PORT}/{db_name}"
            return
        env_db_url = os.getenv("POSTGRES_URL")
        db_name = settings.DB_NAME
        if db_name and env_db_url:
            warning("DB_NAME ignored since POSTGRES_URL is set in environment.")
            self.db_url = env_db_url
            return
        if env_db_url:
            self.db_url = env_db_url
            return
        if db_name:
            self.db_url = f"postgresql://{user}:{password}@localhost:{settings.DB_PORT}/{db_name}"
            return
        raise ValueError("Must specify either db_name or db_url, or set POSTGRES_URL or DB_NAME in environment.")

    def query_to_df(self, sql_query: str, params: tuple|dict = ()) -> pd.DataFrame:
        """
        Execute an SQL query and return results as a Pandas DataFrame.
        
        :param sql_query: The SQL query string.
        :param params: Optional tuple of parameters for parameterized queries.
        :return: Pandas DataFrame with query results.
        """
        return pd.read_sql_query(text(sql_query), self.engine, params=params)

# END
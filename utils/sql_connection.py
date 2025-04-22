import time
from typing import Generator, Iterable
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import pyodbc
import pandas as pd
from tqdm import tqdm
import json
import os

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

def retry_to_sql(chunk, session, tbl_nm, schema, dtypes, replace):
    """Attempts to insert a chunk with retry logic."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            chunk.to_sql(
                con=session.connection(),
                name=tbl_nm,
                schema=schema,
                if_exists=replace,
                index=False,
                dtype=dtypes,
                method="multi"
            )
            return
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {e}") from e

def retry_to_sql_append(chunk, session, tbl_nm, schema, dtypes):
    """Attempts to append a chunk with retry logic."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            chunk.to_sql(
                con=session.connection(),
                name=tbl_nm,
                schema=schema,
                if_exists="append",
                index=False,
                dtype=dtypes,
                method="multi"
            )
            return
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {e}") from e
class PicHorneDashesConnection:
    def __init__(self):
        driver = "{ODBC Driver 17 for SQL Server}"
        # Load the configuration file
        config_path = os.path.join(os.path.dirname(__file__), "config_partners_in_care.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        # Extract the password from the configuration
        sql_server_config = config.get("sql_server", {})
        server_name = sql_server_config.get("server_name")
        database_name = sql_server_config.get("database_name")
        username = sql_server_config.get("username")
        password = sql_server_config.get("password")

        if not all([server_name, database_name, username, password]):
            raise ValueError("Incomplete SQL Server configuration in the configuration file.")

        connection_string = (
            f"DRIVER={driver};"
            f"SERVER={server_name};"
            f"PORT=1433;"
            f"DATABASE={database_name};"
            f"UID={username};"
            f"PWD={password};"
            f"timeout=60"
        )

        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string}
        )

        max_retries = 3
        retry_delay = 60  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                self.engine = create_engine(connection_url, fast_executemany=True)
                self.conn = self.engine.connect()
                break  # Successful connection
            except (pyodbc.OperationalError, OperationalError, SQLAlchemyError) as e:
                if attempt < max_retries:
                    print(f"[Attempt {attempt}] Database connection failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError(f"Failed to connect to database after {max_retries} attempts: {e}") from e
                


    def get_connection(self):

        return self.conn




    def insert_with_progress(self, df: pd.DataFrame, schema: str, tbl_nm: str, dtypes: dict, chunksize: int = 10000) -> None:
        Session = scoped_session(sessionmaker(bind=self.engine))
        session = Session()
        try:
            with tqdm(total=len(df)) as pbar:
                for i, cdf in enumerate(self.__chunker__(df, chunksize)):
                    replace = "replace" if i == 0 else "append"
                    retry_to_sql(cdf, session, tbl_nm, schema, dtypes, replace)
                    pbar.update(len(cdf))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while inserting data: {e}") from e
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An unexpected error occurred: {e}") from e
        finally:
            session.close()
            Session.remove()


    def append_with_progress(self, df: pd.DataFrame, schema: str, tbl_nm: str, dtypes: dict, chunksize: int = 10000) -> None:
        Session = scoped_session(sessionmaker(bind=self.engine))
        session = Session()
        try:
            with tqdm(total=len(df)) as pbar:
                for _, cdf in enumerate(self.__chunker__(df, chunksize)):
                    retry_to_sql_append(cdf, session, tbl_nm, schema, dtypes)
                    pbar.update(len(cdf))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"An error occurred while appending data: {e}") from e
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An unexpected error occurred: {e}") from e
        finally:
            session.close()
            Session.remove()


    def __chunker__(self, seq: Iterable, size: int) -> Generator:
        """
        Split a sequence into chunks of the specified size.

        Args:
            seq (Iterable): The sequence to be chunked.
            size (int): The size of each chunk.

        Returns:
            Generator: A generator yielding chunks of the input sequence.
        """
        return (seq[pos : pos + size] for pos in range(0, len(seq), size))

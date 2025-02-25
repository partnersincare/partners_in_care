from typing import Generator, Iterable
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from tqdm import tqdm


class PicHorneDashesConnection:
    def __init__(self):
        self.engine = create_engine(
            "mssql+pyodbc://@localhost/HORNEDASHES?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )
        self.conn = self.engine.connect()

    def get_connection(self):

        return self.conn

    def insert_with_progress(
        self,
        df: pd.DataFrame,
        schema: str,
        tbl_nm: str,
        dtypes: dict,
        chunksize: int = 10000,
    ) -> None:
        """
        Insert data into a database table with progress tracking.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be inserted.
            schema (str): The schema of the table.
            tbl_nm (str): The name of the table.
            dtypes (dict): Data types for columns.
            chunksize (int, optional): Chunk size for processing. Defaults to 10000.

        Raises:
            RuntimeError: If an error occurs while inserting data.
        """
        Session = scoped_session(sessionmaker(bind=self.engine))
        session = Session()
        try:
            with tqdm(total=len(df)) as pbar:
                for i, cdf in enumerate(self.__chunker__(df, chunksize)):
                    replace = "replace" if i == 0 else "append"
                    cdf.to_sql(
                        con=session.connection(),
                        name=tbl_nm,
                        schema=schema,
                        if_exists=replace,
                        index=False,
                        dtype=dtypes,
                    )
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

    def append_with_progress(
        self,
        df: pd.DataFrame,
        schema: str,
        tbl_nm: str,
        dtypes: dict,
        chunksize: int = 10000,
    ) -> None:
        """
        Append data into a database table with progress tracking.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be appended.
            schema (str): The schema of the table.
            tbl_nm (str): The name of the table.
            dtypes (dict): Data types for columns.
            chunksize (int, optional): Chunk size for processing. Defaults to 10000.

        Raises:
            RuntimeError: If an error occurs while appending data.
        """
        Session = scoped_session(sessionmaker(bind=self.engine))
        session = Session()
        try:
            with tqdm(total=len(df)) as pbar:
                for _, cdf in enumerate(self.__chunker__(df, chunksize)):
                    replace = "append"
                    cdf.to_sql(
                        con=session.connection(),
                        name=tbl_nm,
                        if_exists=replace,
                        index=False,
                        schema=schema,
                        dtype=dtypes,
                    )
                    pbar.update(chunksize)
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

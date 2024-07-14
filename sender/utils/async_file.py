from abc import ABC, abstractmethod
import pandas as pd
from .wrappers import run_in_thread_pool


class ReadFile(ABC):
    @abstractmethod
    async def read_file(self, content):
        pass


class ReadCsv(ReadFile):
    async def read_file(self, content):
        df = await run_in_thread_pool(pd.read_excel, content)
        return self.replace_nan_to_none(df)

    def replace_nan_to_none(self, df):
        return df.where(pd.notnull(df), None)

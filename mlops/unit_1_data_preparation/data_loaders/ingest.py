import requests
from io import BytesIO
from typing import List

import pandas as pd
import numpy as np

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def ingest_files(**kwargs) -> pd.DataFrame:
    dfs: List[pd.DataFrame] = []

    for year, months in [(2024, (1, 3))]:
        for i in range(*months):
            response = requests.get(
                'https://github.com/mage-ai/datasets/raw/master/taxi/green'
                f'/{year}/{i:02d}.parquet'
            )

            if response.status_code != 200:
                raise Exception(response.text)

            df = pd.read_parquet(BytesIO(response.content))

            # Fix to show time series bar chart in Mage 
            # - P.S. Use 'lpep_pickup_datetime_cleaned' as metrics instead of lpep_pickup_datetime
            df['lpep_pickup_datetime_cleaned'] = df['lpep_pickup_datetime'].astype(np.int64) // 10**9

            dfs.append(df)

    return pd.concat(dfs)
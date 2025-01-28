
from time import time

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import pyarrow
import os
import argparse


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_name = 'output_parquet.parquet'

    os.system(f'wget {url} -O {parquet_name}')



    df = pd.read_parquet(f'{parquet_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print(pd.io.sql.get_schema(df, table_name, con=engine))


    df.to_sql(name=table_name, con = engine, if_exists='append')


if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description='ingest CSV data to Postgres')


    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db for postgres')
    parser.add_argument('--table_name', help='tablename for postgres')
    parser.add_argument('--url', help='url for postgres')

    args = parser.parse_args()
    main(args)
    print('done!')
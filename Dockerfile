FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow argparse

WORKDIR /app

copy data-loading-parquet.py data-loading-parquet.py

ENTRYPOINT [ "python", "data-loading-parquet.py"]
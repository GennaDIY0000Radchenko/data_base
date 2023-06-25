import csv
import sys

import pandas as pd
import psycopg2

import requests
import py7zr

import time
import os

username = 'postgres'
password = '314159265'
database = 'data_base'
host = 'data_base'
port = '5432'


def main():
    global username, password, database, host, port
    start_time = time.time()
    print("Start time: ", time.strftime("%H:%M:%S"))

    # download_data(["2019", "2020"])

    file_name_data_2019 = 'data2019.csv'
    file_name_data_2020 = 'data2020.csv'

    data2019 = pd.read_csv(file_name_data_2019, encoding='utf-8', sep=',', low_memory=False, decimal='.')
    data2020 = pd.read_csv(file_name_data_2020, encoding='utf-8', sep=',', low_memory=False, decimal='.')
    data2019 = change_df(data2019)
    data2020 = change_df(data2020)
    data2019['year'] = 2019
    data2020['year'] = 2020

    if does_table_exist():
        print("Table already exist")
    else:
        print("Creating table")
        create_table()

    conn = connect_to_db()
    insert_data_in_db(data2019, conn, 2019)
    conn = connect_to_db()
    insert_data_in_db(data2020, conn, 2020)

    make_request()

    save_time(start_time)
    conn.close()
    print(f"Run in {time.time() - start_time} seconds")


def connect_to_db(attempts=10, sec_sleep=5):
    for _ in range(attempts):
        try:
            connection = psycopg2.connect(user=username, password=password, dbname=database, port=port, host=host)
            print("Connection to database. Success.")
            return connection
        except psycopg2.Error as exception:
            print(f"Exception in connect_to_db:\n{exception}")
            print(f"Connection to database. Fail. Wait {sec_sleep} sec.")
            time.sleep(sec_sleep)

    print("Failed to connect. Try later. Exit.")
    sys.exit()


def download_data(years):
    for year in years:
        if int(year) < 2022:
            url = "https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO" + year + ".7z"
        else:
            url = "https://zno.testportal.com.ua/yearstat/uploads/OpenDataNMT" + year + ".7z"

        req = requests.get(url, stream=True)
        if req.status_code == 200:
            filename = f"data{str(year)}.csv"
            with open(filename, 'wb') as f:
                f.write(req.content)
            with py7zr.SevenZipFile(filename, 'r') as archive:
                archive.extractall()

            if os.path.isfile(f"data{str(year)}.csv"):
                os.remove(f"data{str(year)}.csv")
        else:
            print(f'Request failed: {req.status_code}')


def does_table_exist():
    conn = connect_to_db()
    cur = conn.cursor()
    query = """SELECT COUNT(table_name) FROM information_schema.tables WHERE table_schema LIKE 'public' AND table_type LIKE 'BASE TABLE' AND table_name = 'zno_results'"""
    cur.execute(query)
    result = cur.fetchall()[0][0]
    if result == 1:
        return True
    return False


def change_df(df):
    df.columns = map(str.lower, df.columns)
    for col in df.columns:
        if "ball100" in col:
            df[col] = df[col].apply(pd.to_numeric)
    return df


def create_table():
    conn = connect_to_db()
    with conn:
        cur = conn.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS zno_results(
                outid  VARCHAR NOT NULL,
                birth  NUMERIC NOT NULL,
                sextypename  VARCHAR NOT NULL,
                regname  VARCHAR NOT NULL,
                areaname  VARCHAR NOT NULL,
                tername  VARCHAR NOT NULL,
                regtypename  VARCHAR NOT NULL,
                tertypename  VARCHAR NOT NULL,
                classprofilename  VARCHAR NOT NULL,
                classlangname  VARCHAR NOT NULL,
                eoname  VARCHAR NOT NULL,
                eotypename  VARCHAR NOT NULL,
                eoregname  VARCHAR NOT NULL,
                eoareaname  VARCHAR NOT NULL,
                eotername  VARCHAR NOT NULL,
                eoparent  VARCHAR NOT NULL,
                ukrtest  VARCHAR,
                ukrteststatus  VARCHAR,
                ukrball100  DECIMAL,
                ukrball12  NUMERIC,
                ukrball  NUMERIC,
                ukradaptscale  NUMERIC,
                ukrptname  VARCHAR,
                ukrptregname  VARCHAR,
                ukrptareaname  VARCHAR,
                ukrpttername  VARCHAR,
                histtest  VARCHAR,
                histlang  VARCHAR,
                histteststatus  VARCHAR,
                histball100  DECIMAL,
                histball12  NUMERIC,
                histball  NUMERIC,
                histptname  VARCHAR,
                histptregname  VARCHAR,
                histptareaname  VARCHAR,
                histpttername  VARCHAR,
                mathtest  VARCHAR,
                mathlang  VARCHAR,
                mathteststatus  VARCHAR,
                mathball100  DECIMAL,
                mathball12  NUMERIC,
                mathball  NUMERIC,
                mathptname  VARCHAR,
                mathptregname  VARCHAR,
                mathptareaname  VARCHAR,
                mathpttername  VARCHAR,
                phystest  VARCHAR,
                physlang  VARCHAR,
                physteststatus  VARCHAR,
                physball100  DECIMAL,
                physball12  NUMERIC,
                physball  NUMERIC,
                physptname  VARCHAR,
                physptregname  VARCHAR,
                physptareaname  VARCHAR,
                physpttername  VARCHAR,
                chemtest  VARCHAR,
                chemlang  VARCHAR,
                chemteststatus  VARCHAR,
                chemball100  DECIMAL,
                chemball12  NUMERIC,
                chemball  NUMERIC,
                chemptname  VARCHAR,
                chemptregname  VARCHAR,
                chemptareaname  VARCHAR,
                chempttername VARCHAR,
                biotest  VARCHAR,
                biolang  VARCHAR,
                bioteststatus  VARCHAR,
                bioball100  DECIMAL,
                bioball12  NUMERIC,
                bioball  NUMERIC,
                bioptname  VARCHAR,
                bioptregname  VARCHAR,
                bioptareaname  VARCHAR,
                biopttername  VARCHAR,
                geotest  VARCHAR,
                geolang  VARCHAR,
                geoteststatus  VARCHAR,
                geoball100  DECIMAL,
                geoball12  NUMERIC,
                geoball  NUMERIC,
                geoptname  VARCHAR,
                geoptregname  VARCHAR,
                geoptareaname  VARCHAR,
                geopttername  VARCHAR,
                engtest  VARCHAR,
                engteststatus  VARCHAR,
                engball100  DECIMAL,
                engball12  DECIMAL,
                engdpalevel  VARCHAR,
                engball  NUMERIC,
                engptname  VARCHAR,
                engptregname  VARCHAR,
                engptareaname  VARCHAR,
                engpttername  VARCHAR,
                fratest  VARCHAR,
                frateststatus  VARCHAR,
                fraball100  DECIMAL,
                fraball12  NUMERIC,
                fradpalevel  VARCHAR,
                fraball  NUMERIC,
                fraptname  VARCHAR,
                fraptregname  VARCHAR,
                fraptareaname  VARCHAR,
                frapttername  VARCHAR,
                deutest  VARCHAR,
                deuteststatus  VARCHAR,
                deuball100  DECIMAL,
                deuball12  NUMERIC,
                deudpalevel  VARCHAR,
                deuball  NUMERIC,
                deuptname  VARCHAR,
                deuptregname  VARCHAR,
                deuptareaname VARCHAR,
                deupttername  VARCHAR,
                spatest  VARCHAR,
                spateststatus  VARCHAR,
                spaball100  DECIMAL,
                spaball12  NUMERIC,
                spadpalevel  VARCHAR,
                spaball  NUMERIC,
                spaptname  VARCHAR,
                spaptregname  VARCHAR,
                spaptareaname  VARCHAR,
                spapttername  VARCHAR,
                umltest  VARCHAR,
                umlteststatus  VARCHAR,
                umlball100  DECIMAL,
                umlball12  NUMERIC,
                umlball  NUMERIC,
                umladaptscale  NUMERIC,
                umlptname  VARCHAR,
                umlptregname  VARCHAR,
                umlptareaname  VARCHAR,
                umlpttername  VARCHAR,
                ukrsubtest  VARCHAR,
                mathdpalevel  VARCHAR,
                mathsttest  VARCHAR,
                mathstlang  VARCHAR,
                mathstteststatus  VARCHAR,
                mathstball12  NUMERIC,
                mathstball  NUMERIC,
                mathstptname  VARCHAR,
                mathstptregname  VARCHAR,
                mathstptareaname  VARCHAR,
                mathstpttername  VARCHAR,
                year  NUMERIC NOT NULL
            );
            """
        cur.execute(query)


def last_load(connection, year, attempts=10):
    for _ in range(attempts):
        try:
            cur = connection.cursor()
            cur.execute(f"SELECT COUNT(*) FROM zno_results WHERE year={str(year)}")
            offset = cur.fetchall()[0][0]
            return offset

        except psycopg2.Error as exception:
            print(f"Exception in last_load:\n{exception}")
            connection = connect_to_db()
            continue

    print("Failed last_load. Try later. Exit.")
    sys.exit()


def insert_data_in_db(data, connection, year):
    columns = [i.lower() for i in data.columns]
    placeholders = ','.join(['%s' for _ in range(len(columns))])
    columns = ', '.join(columns)
    offset = last_load(connection, year)
    size = 200

    while offset <= len(data):
        lines = data.iloc[offset:offset + size]
        if lines.shape[0] == 0:
            break
        print(f'Rows: [{offset}:{offset + lines.shape[0]}]', lines, sep="\n")
        values = [tuple(row) for _, row in lines.iterrows()]
        insert_query = f"INSERT INTO zno_results ({columns}) VALUES ({placeholders})"
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            print(f'Load rows: [{offset}:{offset + lines.shape[0]}]')
            cursor.executemany(insert_query, values)
            connection.commit()
            offset += lines.shape[0]
            cursor.close()

        except Exception as e:
            print(e)
            time.sleep(5)
            offset = last_load(connection, year)
            continue

    print(f"Total rows: {offset}")


def make_request():
    conn = connect_to_db()
    query_res = """
                    SELECT
                      regname,
                      AVG(CASE WHEN year = 2019 THEN mathball100 END) AS bal_2019_year,
                      AVG(CASE WHEN year = 2020 THEN mathball100 END) AS bal_2020_year
                    FROM zno_results WHERE
                      mathteststatus = 'Зараховано'
                    GROUP BY regname;
                """
    cursor = conn.cursor()
    cursor.execute(query_res)
    results = cursor.fetchall()

    with open('output.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['region_name', 'bal_2019_year', 'bal_2020_year'])
        for r in results:
            w.writerow(r)


def save_time(start_time):
    with open('time.csv', 'w', newline='') as f:
        f.write("Run_sec\n")
        f.write(f"{time.time() - start_time}\n")


main()

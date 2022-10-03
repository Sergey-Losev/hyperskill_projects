import pandas as pd
import sqlite3
import json

table_name = "convoy"
sheet_name = 'Vehicles'


def import_file(file_name):
    if file_name.endswith(".xlsx"):
        df = pd.read_excel(file_name, sheet_name=sheet_name, dtype=str)
        file_name = file_name.replace(".xlsx", ".csv")
        df.to_csv(file_name, index=None)
        answer = f"{df.shape[0]} lines were imported to {file_name}" if df.shape[0] != 1 else \
            f"{df.shape[0]} line was imported to {file_name}"
        print(answer)
    else:
        df = pd.read_csv(file_name, dtype=str)

    return df, file_name


def correct_data(df, file_name):
    corrected = 0
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if not df.iloc[i, j].isnumeric():
                cleaned = "".join([ch for ch in df.iloc[i, j] if ch.isdigit()])
                df.iloc[i, j] = cleaned
                corrected += 1

    file_name = file_name.replace(".csv", "[CHECKED].csv")
    df.to_csv(file_name, index=None)
    answer = f"{corrected} cells were corrected in {file_name}" if corrected != 1 else \
        f"{corrected} cells was corrected in {file_name}"
    print(answer)

    return df, file_name


def compute_score(vehicle, route_length):
    score = 6
    fuel_burned = int(vehicle['fuel_consumption']) / 100 * route_length
    score -= fuel_burned // int(vehicle['engine_capacity'])
    if fuel_burned > 230:
        score -= 1
    if int(vehicle['maximum_load']) < 20:
        score -= 2

    return score


def save_to_db(df, file_name):
    file_name = file_name.replace("[CHECKED].csv", ".s3db")
    with sqlite3.connect(file_name) as conn:
        cursor = conn.cursor()

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ( vehicle_id INTEGER PRIMARY KEY"
        for i in range(1, len(df.columns)):
            sql += f", {df.columns[i]} INTEGER NOT NULL"

        sql += ", score INTEGER NOT NULL );"
        cursor.execute(sql)

        params = []
        for i, row in df.iterrows():
            row_with_score = list(map(int, tuple(row)))
            row_with_score.append(compute_score(row, 450))
            params.append(row_with_score)

        sql = f"INSERT OR REPLACE INTO {table_name} VALUES (" + "?," * len(row) + "?);"
        cursor.executemany(sql, params)
        conn.commit()

    answer = f"{df.shape[0]} records were inserted into {file_name}" if df.shape[0] != 1 \
        else f"{df.shape[0]} record was inserted into {file_name}"
    print(answer)

    return file_name


def import_to_json(file_name):
    with sqlite3.connect(file_name) as conn:
        cursor = conn.cursor()
        sql = f"SELECT * FROM {table_name};"
        cursor.execute(sql)
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

    result = [item for item in result if item['score'] > 3]
    for item in result:
        item.pop('score')

    to_export = {table_name: result}
    file_name = file_name.replace(".s3db", ".json")
    with open(file_name, 'w') as json_file:
        json.dump(to_export, json_file)

    answer = f"{len(result)} vehicles were saved into {file_name}" if len(result) != 1 \
        else f"{len(result)} vehicle was saved into {file_name}"
    print(answer)


def import_to_xml(file_name):
    with sqlite3.connect(file_name) as conn:
        sql = f"SELECT * FROM {table_name};"
        df = pd.read_sql(sql, conn)

    file_name = file_name.replace(".s3db", ".xml")
    df = df[df.score < 4]
    df.drop('score', axis=1, inplace=True)
    if df.shape[0] > 0:
        df.to_xml(file_name, index=None, xml_declaration=False, root_name=table_name, row_name='vehicle')
    else:
        with open(file_name, "w") as xml:
            xml.write("<convoy>\n</convoy>")
    answer = f"{df.shape[0]} vehicles were saved into {file_name}" if df.shape[0] != 1 \
        else f"{df.shape[0]} vehicle was saved into {file_name}"
    print(answer)


def main():
    file_name = input("Input file name\n")
    if ".s3db" not in file_name:
        df, file_name = import_file(file_name)
        if "[CHECKED]" not in file_name:
            df, file_name = correct_data(df, file_name)

        file_name = save_to_db(df, file_name)

    import_to_json(file_name)
    import_to_xml(file_name)


if __name__ == "__main__":
    main()

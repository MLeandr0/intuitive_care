import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

def connect_to_db():    
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )

def load_data(file_path, delimiter=";", encoding="utf-8"):
    try:
        return pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def process_financial_data(years, trimesters):
    df_list = []
    for year in years:
        for trimester in trimesters:
            file_path = f"files/{year}/{trimester}T{year}.csv"
            print(f"Loading file: {file_path}")
            df = load_data(file_path)
            if df is not None:
                df_list.append(df)
        print(f"Loading files from {year} finished")
    return pd.concat(df_list, ignore_index=True) if df_list else None

def insert_financial_data(cursor, df):
    if df is not None:
        df["VL_SALDO_INICIAL"] = df["VL_SALDO_INICIAL"].replace({',': '.'}, regex=True).astype(float)
        df["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].replace({',': '.'}, regex=True).astype(float)
        sql = """
            INSERT INTO plano_contas (DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_batch(cursor, sql, df.values)
        print(f"Finished inserting financial data")

def insert_operadora_data(cursor, file_path):
    df = load_data(file_path)
    if df is not None:
        df["Regiao_de_Comercializacao"] = df["Regiao_de_Comercializacao"].fillna(0)
        sql = """
            INSERT INTO operadora_plano_saude (
                REGISTRO_OPERADORA, CNPJ, Razao_Social, Nome_Fantasia, Modalidade,
                Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP,
                DDD, Telefone, Fax, Endereco_eletronico, Representante,
                Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_batch(cursor, sql, df.values.tolist())
        print(f"Finished inserting operadora data")

def main():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    years = [2023, 2024]
    trimesters = [1, 2, 3, 4]
    financial_df = process_financial_data(years, trimesters)
    insert_financial_data(cursor, financial_df)
    insert_operadora_data(cursor, "files/Relatorio_cadop.csv")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_dotenv()
    main()
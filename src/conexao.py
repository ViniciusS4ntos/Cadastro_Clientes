import mysql.connector
from mysql.connector import errorcode

def conectar():
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "cadastro_clientes"
    }

    try:
        conn = mysql.connector.connect(**config)
        return conn

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco não encontrado. Criando banco...")

            conn = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"]
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS cadastro_clientes DEFAULT CHARACTER SET 'utf8'")
            cursor.close()
            conn.close()
            print("Banco criado com sucesso!")

            # reconectar e criar tabela
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    telefone VARCHAR(20)
                )
            """)
            conn.commit()
            cursor.close()
            return conn
        else:
            print(f"Erro ao conectar: {err}")
            return None

from conexao import conectar
import re

def cadastrar_cliente(nome, email, telefone):
    # remove tudo que não for número
    telefone_limpo = re.sub(r'\D', '', telefone)

    if not telefone_limpo:
        print("❌ Telefone inválido. Digite apenas números.")
        return

    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome.title(), email.lower(), telefone_limpo)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Cliente cadastrado com sucesso!")
    else:
        print("❌ Falha ao conectar ao banco.")


if __name__ == "__main__":
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone (apenas números): ")
    cadastrar_cliente(nome, email, telefone)

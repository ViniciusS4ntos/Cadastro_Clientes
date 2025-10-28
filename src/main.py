from cadastrar import cadastrar_cliente
from conexao import conectar

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()

    if resultados:
        print("\n=== Lista de Clientes ===")
        for cliente in resultados:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]}")
    else:
        print("Nenhum cliente cadastrado ainda.")
    
    cursor.close()
    conn.close()


def editar_cliente():
    listar_clientes()
    id_cliente = input("\nDigite o ID do cliente que deseja editar: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
    cliente = cursor.fetchone()

    if not cliente:
        print("❌ Nenhum cliente encontrado com esse ID.")
        cursor.close()
        conn.close()
        return

    print(f"\nEditando cliente: {cliente[1]} ({cliente[2]})")

    novo_nome = input("Novo nome (deixe vazio para manter o mesmo): ").strip()
    novo_email = input("Novo email (deixe vazio para manter o mesmo): ").strip()
    novo_telefone = input("Novo telefone (deixe vazio para manter o mesmo): ").strip()

    # se o usuário deixar o campo em branco, mantém o valor atual
    nome_final = novo_nome.title() if novo_nome else cliente[1]
    email_final = novo_email.lower() if novo_email else cliente[2]
    telefone_final = novo_telefone if novo_telefone else cliente[3]

    cursor.execute("""
        UPDATE clientes
        SET nome = %s, email = %s, telefone = %s
        WHERE id = %s
    """, (nome_final, email_final, telefone_final, id_cliente))
    conn.commit()

    print("✅ Cliente atualizado com sucesso!")

    cursor.close()
    conn.close()



def remover_cliente():
    listar_clientes()
    id_cliente = input("\nDigite o ID do cliente que deseja remover: ")

    conn = conectar()
    cursor = conn.cursor()

    # verifica se o cliente existe
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
    cliente = cursor.fetchone()

    if not cliente:
        print("❌ Nenhum cliente encontrado com esse ID.")
        cursor.close()
        conn.close()
        return

    # confirmação antes de remover
    confirmar = input(f"Tem certeza que deseja remover '{cliente[1]}'? (s/n): ").strip().lower()
    if confirmar != 's':
        print("❎ Operação cancelada.")
        cursor.close()
        conn.close()
        return

    cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
    conn.commit()

    print(f"🗑️ Cliente '{cliente[1]}' removido com sucesso!")

    cursor.close()
    conn.close()


def menu():
    while True:
        print("\n=== Sistema de Cadastro de Clientes ===")
        print("1 - Cadastrar novo cliente")
        print("2 - Listar clientes")
        print("3 - Editar cliente")
        print("4 - Remover cliente")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            cadastrar_cliente(nome, email, telefone)

        elif opcao == "2":
            listar_clientes()

        elif opcao == "3":
            editar_cliente()

        elif opcao == "4":
            remover_cliente()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    menu()

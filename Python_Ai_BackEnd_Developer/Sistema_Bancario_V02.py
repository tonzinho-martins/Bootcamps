
def menu():
    menu = """\n
    ============ BANCO PYTHON ===========
    [1]  Depositar
    [2]  Sacar
    [3]  Extrato
    [4]  Cadastrar Nova Conta
    [5]  Listar Contas
    [6]  Listar Usuários
    [7]  Novo Atendimento
    [8]  Cadastrar Novo Usuário
    [9]  Sair
"""
    return print(menu) 

contador_conta = 1000
contador_agencia = 1
lista_usuarios = []
lista_contas = []



def validar_cpf(cpf):
    try:
        cpf_num = int(cpf)
        if len(cpf) == 11:
            return True
            
        else:
            print("ERRO. O CPF deve conter 11 digitos")
            
    except ValueError:
        print("Erro. O CPF deve conter apenas numeros")

def filtrar_usuarios(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
        
def criar_usuario(cpf, usuarios):
        nome = input("Nome: ")
        usuario = {"nome": nome, "cpf": cpf}
        usuarios.append(usuario)
        print("\nUsuário cadastrado com sucesso\n")
  
def criar_conta(cpf, usuarios,contas, numero_conta, agencia):
    
    global contador_conta, contador_agencia
    numero_conta = f"{contador_conta}"
    agencia = f"000{contador_agencia}"

    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            nova_conta = {'numero_conta': numero_conta, 'agencia': agencia, 'saldo': 0, 'extrato': '','qtde_saques': 0}
            for conta in contas:
                if conta['cpf'] == cpf:
                    conta['total_contas_usuario'].append(nova_conta)
                    print("\nNova conta cadastrada com sucesso")
                    contador_conta += 1
                    return True
            conta_usuario = {'nome': usuario['nome'],
                             'cpf': cpf,
                             'total_contas_usuario': [nova_conta],
                             }
            contas.append(conta_usuario)
            print("\nConta cadastrada com sucesso")
            contador_conta += 1;
            return True
    
def listar_contas(usuario,contas):
    if len(contas) == 0:
        print("Nenhuma conta registrada ainda!")
    else:
        for usuario in contas:
            print(f"| {'Nome':<20} | {'CPF':<40}     |")
            print(f"| {usuario['nome']:<20} | {usuario['cpf']:<40}     |")
            print("+----------------------+----------------------------------------------+")
            print(f"| {'Nº Conta':<20} | {'Agência':<20} | {'Saldo':<20}  |")
            print("+----------------------+----------------------------------------------+")
            for conta in usuario['total_contas_usuario']:
                print(f"| {conta['numero_conta']:<20} | {conta['agencia']:<20} | R${conta['saldo']:<20}|")
                print("+----------------------+----------------------------------------------+")
            print("="*71)
        



def listar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("Nenhum usuario registrado!")
    else:
        print("\nLista de Usuários\n")
        print("+------------+-----------------+")
        print(f"| {'Nome':<10} | {'CPF':<15} |")
        print("+------------+-----------------+")
        for usuario in usuarios:
            print(f"| {usuario['nome']:<10} | {usuario['cpf']:<15} |")
            print("+------------+-----------------+")
            

def depositar(cpf,contas,valor_deposito,numero_conta):
    for usuario in contas:
        if usuario['cpf'] == cpf:
            for conta in usuario['total_contas_usuario']:         
                if int(numero_conta) == int(conta['numero_conta']):
                    conta['saldo'] += float(valor_deposito)
                    conta['extrato'] += f"Depósito: R${float(valor_deposito)}\n"
                    print("Depósito realizado com sucesso")
                    return True
    
def sacar(cpf,contas,numero_conta,valor_saque):
    LIMITE_SAQUES = 3
    LIMITE_VALOR_SAQUE = 500
    for usuario in contas:
        if usuario['cpf'] == cpf:
            for conta in usuario['total_contas_usuario']:
                if int(numero_conta) == int(conta['numero_conta']):
                    excedeu_saldo = float(valor_saque) > conta['saldo']
                    excedeu_limite = float(valor_saque) > LIMITE_VALOR_SAQUE
                    excedeu_saque = conta['qtde_saques'] >= LIMITE_SAQUES

                    if excedeu_saldo:
                        print("Erro! Você não possui saldo suficiente!")
                    elif excedeu_limite:
                        print("Erro! Valor máximo de saque é de R$ 500,00")
                    elif excedeu_saque:
                        print("Erro! Você já atingiu o limite diário de saques")
                    elif conta['saldo'] > 0:
                        conta['saldo'] -= float(valor_saque)
                        conta['qtde_saques'] += 1
                        print("Saque realizado com sucesso")
                        conta['extrato'] += f"Saque: R${float(valor_saque)}\n"
                        return
        
def exibir_extrato(cpf, contas, numero_conta):
    for usuario in contas:
        if usuario['cpf'] == cpf:
            for conta in usuario['total_contas_usuario']:
                if int(numero_conta) == int(conta['numero_conta']):
                    if conta['extrato'] == '':
                        print("Nenhuma transação registrada")
                        break
                    else:
                        print(f"\nExtrato:\n{conta['extrato']}")
                        print(f"Saldo: R${conta['saldo']}")
                        return

def continuar_atendimento():
    while True:
        resposta = input("Deseja continuar? [S]/[N]: ").upper()
        if "S" == resposta:
            menu()
            selecionar_opcao()
        elif "N" == resposta:
            print("Volte sempre! Obrigado")
            break
        else:
            print("Erro! Resposta inválida.")
               
def selecionar_opcao():
    while True:
        opcao = input("Selecione uma opção: ")
        try:
            opcao_num = int(opcao)
            if opcao_num == 1:
                while True:
                    cpf = input("CPF: ")
                    if validar_cpf(cpf):
                        break
                if len(lista_contas) == 0:
                    print("Nenhuma conta registrada!")
                for usuario in lista_contas:
                    if usuario['cpf'] == cpf:
                        print(f"| {'Nome':<20} | {'CPF':<40}     |")
                        print(f"| {usuario['nome']:<20} | {usuario['cpf']:<40}     |")
                        print("+----------------------+----------------------------------------------+")
                        print(f"| {'Nº Conta':<20} | {'Agência':<20} | {'Saldo':<20}  |")
                        print("+----------------------+----------------------------------------------+")
                        for conta in usuario['total_contas_usuario']:
                            print(f"| {conta['numero_conta']:<20} | {conta['agencia']:<20} | R${conta['saldo']:<20}|")
                            print("+----------------------+----------------------------------------------+")
                        print("="*71)
                        numero_conta = input("Nº Conta: ")
                        valor_deposito = input("Valor depósito R$: ")
                        depositar(cpf, lista_contas,valor_deposito,numero_conta)
                        return
                    else:
                        print("Nenhuma conta registrada para este CPF")
                        print("Cadastre uma nova conta para efetuar operações")
                        break
                break
        
            if opcao_num == 2:
                while True:
                    cpf = input("CPF: ")
                    if validar_cpf(cpf):
                        break
                if len(lista_contas) == 0:
                    print("Nenhuma conta registrada!")
                for usuario in lista_contas:
                    if usuario['cpf'] == cpf:
                        print(f"| {'Nome':<20} | {'CPF':<40}     |")
                        print(f"| {usuario['nome']:<20} | {usuario['cpf']:<40}     |")
                        print("+----------------------+----------------------------------------------+")
                        print(f"| {'Nº Conta':<20} | {'Agência':<20} | {'Saldo':<20}  |")
                        print("+----------------------+----------------------------------------------+")
                        for conta in usuario['total_contas_usuario']:
                            print(f"| {conta['numero_conta']:<20} | {conta['agencia']:<20} | R${conta['saldo']:<20}|")
                            print("+----------------------+----------------------------------------------+")
                        print("="*71)
                        numero_conta = input("Nº Conta: ")
                        valor_saque = input("Valor Saque R$: ")
                        sacar(cpf,lista_contas,numero_conta,valor_saque)
                        break
                    else:
                        print("Nenhuma conta registrada para este CPF")
                        print("Cadastre uma nova conta para efetuar operações")
                break
            
            if opcao_num == 3:
                while True:
                    cpf = input("CPF: ")
                    if validar_cpf(cpf):
                        break
                if len(lista_contas) == 0:
                    print("Nenhuma conta registrada!")
                for usuario in lista_contas:
                    if usuario['cpf'] == cpf:
                        print(f"| {'Nome':<20} | {'CPF':<40}     |")
                        print(f"| {usuario['nome']:<20} | {usuario['cpf']:<40}     |")
                        print("+----------------------+----------------------------------------------+")
                        print(f"| {'Nº Conta':<20} | {'Agência':<20} | {'Saldo':<20}  |")
                        print("+----------------------+----------------------------------------------+")
                        for conta in usuario['total_contas_usuario']:
                            print(f"| {conta['numero_conta']:<20} | {conta['agencia']:<20} | R${conta['saldo']:<20}|")
                            print("+----------------------+----------------------------------------------+")
                        print("="*71)
                        numero_conta = input("Nº Conta: ")
                        exibir_extrato(cpf,lista_contas,numero_conta)
                        break
                    else:
                        print("Nenhuma conta registrada para este CPF")
                        print("Cadastre uma nova conta para efetuar operações")
                break
            

            if opcao_num == 4:
                while True:
                    cpf = input("CPF: ")
                    if validar_cpf(cpf):
                        break
                if len(lista_usuarios) == 0:
                    print("Cadastre-se primeiro para conseguir criar uma conta!")
                    break
                if criar_conta(cpf, lista_usuarios, lista_contas, contador_conta, contador_agencia):
                    break
                else:
                    print("Usuário não encontrado!")
                    break

            if opcao_num == 5:
                listar_contas(lista_usuarios,lista_contas)
                break

            if opcao_num == 6:
                listar_usuarios(lista_usuarios)
                break

            if opcao_num == 7:
                menu()
                break

            if opcao_num == 8:
                while True:
                    cpf = input("CPF: ")
                    if validar_cpf(cpf):
                        break
                if filtrar_usuarios(cpf, lista_usuarios):
                    print("Usuário já cadastrado")
                    break
                else:
                    criar_usuario(cpf, lista_usuarios)
                    break

            if opcao_num == 9:
                print("Volte sempre! Obrigado")
                break
            else:
                print("Erro! Digite opção válida")


        except ValueError:
            print("Erro! Opção inválida")

def main():

    print("===== INÍCIO DO SEU ATENDIMENTO =====")
    menu()
    selecionar_opcao()
    continuar_atendimento()
main()

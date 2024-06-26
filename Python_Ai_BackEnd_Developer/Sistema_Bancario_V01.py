saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

print('='*10, 'Banco Python', '='*10)
print('\nMenu Principal\n')
print('[1] Depositar\n[2] Sacar\n[3] Extrato\n[4] Consultar Saldo\n[5] Sair')

while True:
    opcao = input('Informe a opção: ')

    if opcao == '1':
        valor = float(input('Informe o valor do depósito: R$ '))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso")
        else:
            print("Operação falhou! O valor informado é inválido")
    
    elif opcao == '2':
        valor = float(input("Informe o valor do saque: R$ "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso")

    elif opcao == '3':
        print('='*10, 'Extrato', '='*10)
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("="*30)
    elif opcao == '4':
        print(f"\nSeu saldo é de R$ {saldo:.2f}")
    elif opcao == '5':
        print("\nOperações Encerradas.")
        break
    else:
        print("\nOperação inválida! Por favor, selecione novamente a operação desejada.")
        print('\nSelecione uma opção:\n')
        print('[1] Depositar\n[2] Sacar\n[3] Extrato\n[4] Consultar Saldo\n[5] Sair')

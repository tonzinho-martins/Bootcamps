from datetime import datetime
from abc import ABC

class Cliente:
    def __init__(self):
        self.contas = []
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def registrar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf):
        super().__init__()
        self.nome = nome
        self.cpf = cpf
    
class ContaBancaria:
    def __init__(self, cliente, numero_conta):
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._agencia = '0001'
        self._saldo = 0
        self._extrato = Extrato()
    
    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(cliente, numero_conta)
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def extrato(self):
        return self._extrato
    
    def depositar(self, valor):
        valor = float(valor)
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")

        else:
            print("Valor inválido")
            return False
        return True
    
    def sacar(self, valor):
        valor = float(valor)
        excedeu_saldo = valor > self._saldo
        if excedeu_saldo:
            print("Valor excede saldo")

        elif valor <= 0:
            print("Valor inválido")
        else:
            self._saldo -= valor
            print("Saque realizado com sucesso")
            return True
        return False
    
class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero_conta, limite=500, limite_saques=3):
        super().__init__(cliente, numero_conta)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        valor = float(valor)
        numero_saques = len([transacao for transacao in self.extrato.transacoes if transacao["tipo"] == "Saque"])
        excedeu_saques = numero_saques >= self.limite_saques
        excedeu_limite = valor > self.limite

        if excedeu_saques:
            print("Você excedeu o limite de saques")
        elif excedeu_limite:
            print("Valor excede o limite")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\n
        Titular: {self.cliente.nome}
        Agência: {self.agencia}
        C/C: {self.numero_conta}
        """
    
class Extrato:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        })

class Transacao(ABC):
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)
        if transacao_realizada:
            conta.extrato.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)
        if transacao_realizada:
            conta.extrato.adicionar_transacao(self)
        
def menu():
    menu = """\n
    ============ BANCO PYTHON ===========
    [1]  Depositar
    [2]  Sacar
    [3]  Extrato
    [4]  Cadastrar Nova Conta
    [5]  Listar Contas
    [6]  Listar Clientes
    [7]  Consultar Saldo
    [8]  Cadastrar Novo Cliente
    [9]  Sair
"""
    return print(menu) 

def filtrar_cliente(cpf, clientes):
    if clientes:
        for cliente in clientes:
            if cliente.cpf == cpf:
                return cliente
    else:
        print("\n@@@ Nenhum cliente cadastrado ainda. @@@")

def criar_cliente(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n@@@ Erro! Cliente já cadastrado! @@@")
        return
    nome = input("Informe seu nome: ")
    cliente = PessoaFisica(nome, cpf)
    clientes.append(cliente)
    print(f"\n=== Cliente foi cadastrado com sucesso! ===")

def listar_clientes(clientes):
    if not clientes:
        print("\n@@@ Erro! Nenhum cliente cadastrado ainda! @@@")
    else:
        print("\nLista de Clientes\n")
        print("+------------+-----------------+")
        print(f"| {'Nome':<10} | {'CPF':<15} |")
        print("+------------+-----------------+")
        for cliente in clientes:
            print(f"| {cliente.nome:<10} | {cliente.cpf:<15} |")
            print("+------------+-----------------+")

numero_conta = 1000

def cadastrar_conta(clientes, contas):
    global numero_conta
    cpf = input("Informe o CPF: ")
    if not clientes:
        print("\n@@@ Erro! Nenhum cliente cadastrado ainda! @@@")
    elif clientes:
        for cliente in clientes:
            if cliente.cpf == cpf:
                conta = ContaCorrente.nova_conta(numero_conta=numero_conta, cliente=cliente)
                contas.append(conta)
                cliente.contas.append(conta)
                numero_conta += 1
                print("\n=== Conta cadastrada com sucesso! ===")
    else:
        print("\n@@@ Erro! Cliente não cadastrado ainda! @@@")
            
def listar_contas(contas):
    if not contas:
        print("\n@@@ Erro! Nenhuma conta cadastrada ainda! @@@")
        return
    else:
        for conta in contas:
            print("="*30)
            print(str(conta))
            print("="*30)

def depositar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("            ======== Suas Contas =======")
        for conta in cliente.contas:
            print("="*30)
            print(str(conta))
            print("="*30)
        num_conta = input("\n Selecione a conta desejada: ")
        valor = input("Valor do depósito: R$ ")
        for conta in cliente.contas:
            if conta.numero_conta == int(num_conta):
                transacao_deposito = Deposito(valor)
                cliente.registrar_transacao(conta, transacao_deposito)
                
    else:
        print("\n@@@@ Erro! Cliente não encontrado. @@@")
        
def sacar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("            ======== Suas Contas =======")
        for conta in cliente.contas:
            print("="*30)
            print(str(conta))
            print("="*30)
        num_conta = input("\nSelecione a conta desejada: ")
        valor = input("Valor do saque: R$ ")
        for conta in cliente.contas:
            if conta.numero_conta == int(num_conta):
                transacao_saque = Saque(valor)
                cliente.registrar_transacao(conta, transacao_saque)
                
def exibir_extrato(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("            ======== Suas Contas =======")
        for conta in cliente.contas:
            print("="*30)
            print(str(conta))
            print("="*30)
        num_conta = input("Selecione a conta para obter o extrato: ")
        for conta in cliente.contas:
            if conta.numero_conta == int(num_conta):
                print("\n================= EXTRATO ==================")
                transacoes = conta.extrato.transacoes

                extrato = ""
                if not transacoes:
                    extrato = "Não foram realizadas movimentações"
                else:
                    for transacao in transacoes:
                        extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']}"
                        
                print(extrato)
                print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
                print("============================================")

def consultar_saldo(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        if cliente.contas:
            for conta in cliente.contas:
                print(str(conta))

            num_conta = input("\nSelecione a conta para consultar o saldo: ")
            for conta in cliente.contas:
                if conta.numero_conta == int(num_conta):
                    print("===================================")
                    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
                    print("===================================")

def main():
    contas = []
    clientes = []

    while True:
        menu()    
        opcao = input("Opção: ")
        if opcao == '1':
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            cadastrar_conta(clientes, contas)
            
        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            listar_clientes(clientes)  

        elif opcao == '7':
            consultar_saldo(clientes)

        elif opcao == '8':
            criar_cliente(clientes)

        elif opcao == '9':
            print("Obrigado! Volte sempre")
            break
        else:
            print("Opção inválida!\nTente novamente...")

main()




























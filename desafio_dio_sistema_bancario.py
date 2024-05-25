import textwrap

def menu():
    menu = """\n
    ************** MENU *****************

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))

def depositar(*, saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite de saque.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(*, saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_novo_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def criar_nova_conta(contas, usuarios, agencia):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado! Crie um usuário antes de criar uma conta.")
        return

    numero_conta = len(contas) + 1
    contas.append({"numero_conta": numero_conta, "cpf": cpf, "agencia": agencia})

    print(f"Conta número {numero_conta} criada com sucesso!")

def listar_contas(contas, usuarios):
    for conta in contas:
        usuario = filtrar_usuario(conta["cpf"], usuarios)
        print(f"Agência: {conta['agencia']} - Conta: {conta['numero_conta']} - Usuário: {usuario['nome']}")

def main():
    # Inicialização das listas de usuários e contas
    usuarios = []
    contas = []

    saldo = 0
    limite = 500  # Limite de saque por transação
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3  # Limite de saques por dia
    AGENCIA = "0001"  # Constante de agência

    while True:
        opcao = menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo=saldo, extrato=extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                numero_saques=numero_saques,
                limite=limite,
                LIMITE_SAQUES=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo=saldo, extrato=extrato)
        elif opcao == "nc":
            criar_nova_conta(contas=contas, usuarios=usuarios, agencia=AGENCIA)
        elif opcao == "lc":
            listar_contas(contas=contas, usuarios=usuarios)
        elif opcao == "nu":
            criar_novo_usuario(usuarios=usuarios)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()

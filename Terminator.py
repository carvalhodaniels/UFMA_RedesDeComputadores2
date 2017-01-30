# coding=utf-8
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
try:
    server_address = ('localhost', 10005)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
except:
    print "Nao foi possivel conectar ao servidor."
    raw_input()
    sys.exit(0)
cont = 0

# Pergunta se há convites não respondios
def convite(f):
    sock.sendall("PENDENTE")
    convite = sock.recv(32000)
    if convite != "NADA":
        # Trata a mensagem
        convite = str(convite)
        convite = convite.split(', [')
        convitefim = []
        for i in range (len(convite)):
            convite1 = []
            convite1 = convite[i].replace("[", "")
            convite1 = convite1.replace("]", "")
            convitefim.append(convite1)
            resposta = []
        # Percorre os convites
        for i in range(len(convitefim)):
            print "Voce gostaria de participar do seguinte evento: ", convitefim[i], "(S/N)?"
            valor = str(raw_input(": "))
            if valor == "s" or valor == "S":
                resposta.append("1")
                print "Evento aceito com sucesso"
            else:
                resposta.append("2")
                print "Evento recusado com sucesso"
        sock.sendall("RESPOSTA " + str(resposta))
    else:
        if f == "s":
            print "Nao ha nenhum convite a aceitar."

# Pede para realizar login
def login():
    loginerr = -1
    while loginerr != 0:
        print "Sistema de agendas compartilhadas\n" \
              "Insira seu login: "
        login = str(raw_input())
        print "Insira sua senha: "
        senha = str(raw_input())
        sock.sendall("VALIDAR " + login + "/" + senha)
        # Look for the response
        amount_received = 0
        amount_expected = len(login)

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            if data == "VALIDUSER":
                print "Login realizado com sucesso"
                loginerr = 0
                convite("n")
            elif data == "INVALIDUSER":
                print "Login ou senha invalidos"

# Menu!
def menu():
    opt = 1
    while opt != 4:
        print "\nInterface Usuário:\n" \
              "1. Marcar Compromisso\n" \
              "2. Visualizar Compromissos\n" \
              "3. Aceitar Convites\n" \
              "4. Sair\n"
        while True:
            try:
                opt = int(raw_input(': '))  # recebe a opção
                break
            except:
                print "Opção inexistente."
        if opt == 1:
            marcaCompromisso()
        elif opt == 2:
            visualCompromisso()
        elif opt == 3:
            convite("s")
        elif opt == 4:
            sock.close()

# Pede para marcar um compromisso
def marcaCompromisso():
    dataerr = -1
    while dataerr != 0:
        print "Insira a data para marcar o compromisso (DD/MM/AAAA HH:MN DESCRICAO):"
        date = str(raw_input(': '))
        checkdia = date[0:2]
        checkmes = date[3:5]
        checkano = date[6:10]
        #checar se ano, mes e dia é válido
        if int(checkano) < 2017:
            print "Ano impossivel\n"
        else:
            if int(checkmes) > 12 or int(checkmes) < 0:
                print checkmes + ": Mes impossivel\n"
            elif int(checkmes) == 2:
                if not (29 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel1\n"
                else:
                    dataerr = 0
            elif int(checkmes) == 1 or 3 or 5 or 6 or 8 or 10 or 12:
                if not (31 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel2\n"
                else:
                    dataerr = 0
            elif int(checkmes) == 2 or 4 or 6 or 9 or 11:
                if not (30 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel3\n"
                else:
                    dataerr = 0
    # Envia a mensagem
    sock.sendall("COMPROMISSO " + date)
    # Look for the response
    resposta = sock.recv(1024)
    if resposta.find("SALVO") > -1 :

        # Quer adicionar outro usuario ao compromisso?
        print ("Insira as pessoas a serem convidadas separadas por / e 'ninguem' para nao convidar ninguem:")
        convites = raw_input(': ')
        
        if(convites.find("ninguem") > -1):
            sock.sendall('')
        else:
            sock.sendall(convites)
            amount_received = 0
            amount_expected = len("CONVIDADO")
        
            while amount_received < amount_expected:
                data = sock.recv(1024)
                amount_received += len(data)
                if data == "CONVIDADO":
                    print "Convidado com sucesso!"
        
    
# Visualiza os compromissos do usuário
def visualCompromisso():
    sock.sendall("VISUALIZAR")
    compromisso = data = sock.recv(32000)
        
    if compromisso != "NADA":
        #separa a variavel data onde há "], [" em um vetor
        gambis = data.split("], [")
        osgambis = []
        for i in range(len(gambis)):
            #substitui os colchetes por nada
            ogambis = gambis[i].replace("[", "")
            ogambis1 = ogambis.replace("]", "")
            osgambis.append(ogambis1)
        for i in range(len(osgambis)):
            print osgambis[i]
        
    else:
        print "Sem compromissos cadastrados para essa conta." 


login()
menu()

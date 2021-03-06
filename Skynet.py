import threading
import socket
import sys
import time
import mysql.connector

compromissos = []
usuarios = []
atual = ""

# Inicia conex�o com o banco de dados
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
                        password='',database='skynetdb')

# DEFINE O USUARIO
class user:
   login = ""
   senha = ""
   nome = ""
   server_adrr = []

   def __init__(self,nome,server_adrr,login,senha):
      self.nome = nome
      self.server_adrr = server_adrr
      self.login = login
      self.senha = senha


def make_user(nome,server_adrr,login,senha):
   user1 = user(nome,server_adrr,login,senha)
   return user1

# DEFINE O COMPROMISSO
class compromisso(object):
   date = ""
   descricao = ""
   login = ""
   def __init__(self,date,descricao,login):
      self.date = date
      self.login = login
      self.descricao = descricao
      

def make_compromisso(date,descricao,login):
   compromisso1 = compromisso(date,descricao,login)
   return compromisso1


# Salva um compromisso no banco
def salvaCompromisso(login,data1):
   data = data1[12:]                      #12 � o tamanho de "COMPROMISSO "
   date = data[0:16]                      #10 � o tamanho da data
   descricao = data[17:len(data)]         #o resto � a descricao

   c = conn.cursor()
   c.execute("INSERT INTO compromisso(data, descricao) VALUES (STR_TO_DATE('%s','%%d/%%m/%%Y %%H:%%i'),'%s')" % (date, descricao))
   c.execute("INSERT INTO compromisso_conta VALUES ("\
      "(SELECT idconta FROM conta WHERE login = '%s' LIMIT 1),"\
      "(SELECT idcompromisso FROM compromisso WHERE data = (STR_TO_DATE('%s','%%d/%%m/%%Y %%H:%%i')) LIMIT 1), 1)" % (login, date))

   # Salva (commit) as mudan�as
   conn.commit()

# Relaciona outras contas a um compromisso
def mandarConvites(convites,data1):
   c = conn.cursor()
   data = data1[12:]                      #12 � o tamanho de "COMPROMISSO "
   date = data[0:16]                      #10 � o tamanho da data
   for i in range(len(convites)):         #percorre as contas convidadas
      c.execute("INSERT INTO compromisso_conta VALUES ("\
      "(SELECT idconta FROM conta WHERE login = '%s' LIMIT 1),"\
      "(SELECT idcompromisso FROM compromisso WHERE data = (STR_TO_DATE('%s','%%d/%%m/%%Y %%H:%%i')) LIMIT 1), 0)" % (convites[i], date))
      conn.commit()

# Espera uma conex�o
def esperandoConexao():
       try:
           print >> sys.stderr, 'Conexao de', client_address

           # Recebe os dados em pequenos "pacotes"
           while True:
               data = connection.recv(32000)
               print >> sys.stderr, 'Recebeu "%s"' % data
               if data:
                   # Valida login do user
                   if(data.find("VALIDAR") > -1):
                           separator = data.find("/")
                           login = data[8:separator]
                           senha = data[separator+1:]

                           # Pesquisa o login e senha no banco
                           c = conn.cursor()
                           c.execute("SELECT * FROM conta WHERE login = '%s' AND password = '%s'" % (login, senha))
                           # Mostra o primeiro resultado
                           t = c.fetchone()

                           if t is not None:
                              atual = login
                              connection.sendall("VALIDUSER")
                           else:
                              connection.sendall("INVALIDUSER")

                   # Recebe um pedido de criar um compromisso
                   if(data.find("COMPROMISSO") != -1):
                       salvaCompromisso(atual,data)
                       connection.sendall("SALVO")
                       newdata = connection.recv(32000)
                       convites = newdata.split('/')
                       mandarConvites(convites,data)
                       connection.sendall("CONVIDADO")

                   # Recebe um pedido de mostrar os compromissos
                   if(data.find("VISUALIZAR") > -1):
                       c = conn.cursor()
                       c.execute("SELECT DATE_FORMAT(data, '%%d/%%m/%%Y %%H:%%i'),descricao FROM compromisso WHERE idcompromisso IN "\
                       "(SELECT idcompromisso FROM compromisso_conta WHERE idconta = "\
                       "(SELECT idconta FROM conta WHERE login = '%s' LIMIT 1)) ORDER BY data" % (atual))
                       ar = str([[str(item) for item in results] for results in c.fetchall()])
                       if ar != "[]":
                          connection.sendall(ar)
                       else:
                          connection.sendall("NADA")

                   # Recebe um pedido de verificar se h� compromissos a serem confirmados
                   if(data.find("PENDENTE") > -1):
                       c = conn.cursor()
                       c.execute("SELECT DATE_FORMAT(data, '%%d/%%m/%%Y %%H:%%i'),descricao FROM compromisso WHERE idcompromisso IN "\
                                 "(SELECT idcompromisso FROM compromisso_conta WHERE status = 0 AND idconta = "\
                                 "(SELECT idconta FROM conta WHERE login = '%s' LIMIT 1))" % (atual))
                       ar = str([[str(item) for item in results] for results in c.fetchall()])
                       if ar != "[]":
                          connection.sendall(ar)
                       else:
                          connection.sendall("NADA")

                   # Recebe a resposta de um compromisso a ser confirmado ou n�o
                   if(data.find("RESPOSTA") > -1):
                      c = conn.cursor()
                      gambis = data[9:] # retira RESPOSTA da variavel data
                      atual = login
                      #divide a string em um vetor separando onde tem ', '
                      agambis = gambis.split("\', \'") 
                      osgambis = []
                      for i in range(len(agambis)):
                         #substitui os colchetes e aspas simples por nada
                         ogambis = agambis[i].replace("[", "")
                         ogambis1 = ogambis.replace("]", "")
                         ogambis2 = ogambis1.replace("'", "")
                         osgambis.append(ogambis2) # insere tudo em um vetor
                      for i in range(len(osgambis)):
                         c.execute("UPDATE compromisso_conta SET status = '%s' WHERE status = 0 AND "\
                                   "idconta = (SELECT idconta FROM conta WHERE login = '%s')" % (osgambis[i],atual))
                         conn.commit()

               else:
                   print >> sys.stderr, 'Sem mais dados de', client_address
                   break

       finally:
           # Fecha a conexão
           connection.close()
           return


# Criando socket  TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# "Colocando" socket na porta
server_address = ('localhost', 10005)
print >>sys.stderr, 'iniciando em %s na porta %s' % server_address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Ouvindo na porta
sock.listen(1)

# Inicializa��o das threads
while True:
   print >>sys.stderr, 'Esperando conexao'
   # Assim que a conex�o for aceita, cria uma thread para tratar ela
   connection, client_address = sock.accept()
   t1 = threading.Thread(target = esperandoConexao, args = []) 
   t1.start()


"""
Arquivo de configuração para credenciais do banco de dados MySQL
Ajuste as credenciais de acordo com sua instalação
"""

# Configurações de conexão MySQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',           # Usuário do MySQL
    'password': 'Root123.',           # ALTERE AQUI: Coloque sua senha do MySQL
    'database': 'consultas_medicas',
    'port': 3306
}

# Instruções de uso:
# 1. Descubra sua senha do MySQL
# 2. Altere o campo 'password' acima
# 3. Salve este arquivo
# 4. Execute novamente: python test_consultas.py

"""
COMO DESCOBRIR/RESETAR A SENHA DO MySQL NO WINDOWS:

OPÇÃO 1 - Se você lembra da senha:
   Simplesmente coloque no campo 'password' acima

OPÇÃO 2 - Resetar a senha do root:
   1. Abra o MySQL Workbench ou prompt de comando
   2. Conecte como root
   3. Execute: ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
   4. Execute: FLUSH PRIVILEGES;
   5. Coloque 'nova_senha' no campo 'password' acima

OPÇÃO 3 - Criar novo usuário (recomendado para desenvolvimento):
   1. Conecte no MySQL como root
   2. Execute:
      CREATE USER 'dev'@'localhost' IDENTIFIED BY 'dev123';
      GRANT ALL PRIVILEGES ON consultas_medicas.* TO 'dev'@'localhost';
      FLUSH PRIVILEGES;
   3. Altere as credenciais acima para:
      'user': 'dev'
      'password': 'dev123'

OPÇÃO 4 - Verificar senha salva no MySQL Workbench:
   1. Abra MySQL Workbench
   2. Veja as conexões salvas
   3. Clique em "Test Connection" para verificar se conecta
   4. Use a mesma senha aqui
"""
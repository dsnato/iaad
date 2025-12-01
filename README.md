# Projeto de Introdução à Análise e Armazenamento de Dados (IAAD)

Este repositório contém a interface desenvolvida em Streamlit para o sistema de gerenciamento de Clientes e Pedidos, integrado a um banco de dados MySQL. A aplicação permite realizar operações CRUD, visualizar dados e navegar facilmente entre as funcionalidades.

## Pré-requisitos

- Python 3.10+ instalado
- MySQL ou MariaDB rodando localmente

## Instalação de dependências

Abra um terminal PowerShell no diretório do projeto e execute:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Criar banco de dados e carregar esquema

O arquivo `consultas_medicas.sql` já contém a criação do schema `consultas_medicas`, tabelas, dados iniciais e triggers. Para aplicá-lo no seu servidor MySQL local execute (substitua `root` pelo seu usuário se necessário):

```powershell
mysql -u root -p < consultas_medicas.sql
```

Ao executar o comando acima, será solicitado a senha do usuário MySQL; o script criará o schema e o povoará com os dados de exemplo.

## Configurar credenciais do banco

Por simplicidade o projeto atualmente configura a conexão em `app_streamlit.py` na linha onde `MySQLDB` é instanciado. Edite `app_streamlit.py` e ajuste os parâmetros `host`, `user`, `password` e `database` conforme o seu ambiente. Exemplo:

```python
from db import MySQLDB
db = MySQLDB(host='localhost', user='root', password='SUA_SENHA', database='consultas_medicas')
```

Se preferir, você pode modificar `db.py` para ler variáveis de ambiente ou usar um arquivo `.env`.

## Executar a aplicação Streamlit

No PowerShell, execute:

```powershell
# dentro da pasta do projeto
streamlit run app_streamlit.py
```

## Testes e uso

- Use a aba "Clientes" para criar, editar e deletar pacientes (mapeados para a tabela `Paciente`).
- Use a aba "Pedidos" -> "Criar" para agendar consultas (mapeadas para `Consulta`).
- Os triggers definidos em `consultas_medicas.sql` irão validar CPF, e-mail e telefones ao inserir/atualizar registros.

## Problemas comuns

- Erro de conexão: verifique usuário/senha e se o servidor MySQL está rodando.
- Permissões: o usuário MySQL precisa de privilégios para criar schema e tabelas ao rodar o script SQL.

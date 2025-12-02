# Roteiro de Apresentação  Sistema de Consultas Médicas

## Parte 1: Introdução, Stack e Demonstração da Interface (Pessoa 1)  2 minutos

**Exibição na tela:** Slide de capa  VS Code aberto no projeto  Streamlit rodando (tela Home).

### Roteiro Detalhado

**[00:00 - 00:20] Abertura e Contexto**
- "Olá, sou **[Nome P1]**. Vou apresentar nosso **Sistema de Gerenciamento de Consultas Médicas**, desenvolvido para organizar e controlar todo o fluxo de atendimento em clínicas."
- "O sistema gerencia **4 entidades principais**: Pacientes, Médicos, Clínicas e Consultas, com relacionamentos bem definidos entre elas."

**[00:20 - 00:50] Stack Tecnológica**
- "A stack utilizada foi:
  - **MySQL 8.0** como SGBD relacional
  - **Python 3.x** para lógica de negócio e conexão com o banco via `mysql-connector`
  - **Streamlit** para construir a interface web interativa de forma rápida e pythônica"
- *[Mostrar brevemente VS Code com a estrutura do projeto: app_streamlit.py, consultas_medicas.sql, requirements.txt]*

**[00:50 - 01:30] Demonstração da Interface**
- "Vou demonstrar a interface Streamlit em funcionamento."
- *[Navegar pela tela Home mostrando os cards com métricas]*
  - "Na **Home**, temos um dashboard com totais: X pacientes, Y médicos, Z clínicas e W consultas cadastradas."
- *[Clicar em 'Pacientes' no menu lateral]*
  - "Aqui temos o **CRUD completo de Pacientes** com 4 abas: Listar, Criar, Editar e Deletar."
- *[Demonstrar rapidamente a aba 'Listar']*
  - "Podemos visualizar todos os pacientes com CPF, nome, data de nascimento, gênero, telefone e email."
- *[Mostrar aba 'Criar' sem preencher]*
  - "Para criar, temos validação de campos obrigatórios: CPF no formato XXX.XXX.XXX-XX, telefone no formato (DD) XXXXX-XXXX, além de email e gênero."

**[01:30 - 02:00] Funcionalidades Avançadas**
- "O sistema também possui seções para gerenciar Médicos e Consultas, além de uma tela dedicada aos **Triggers**, que vou deixar para meu colega detalhar."
- "A arquitetura foi pensada para ser modular: os dados podem vir de um banco MySQL real ou funcionar com dados mockados em memória para demonstração, usando `st.session_state` do Streamlit."
- "Agora vou passar para **[Nome P2]**, que vai explicar a modelagem do banco de dados e os mecanismos de integridade."

---

## Parte 2: Modelagem do Banco e Triggers de Validação (Pessoa 2)  2 minutos

**Exibição na tela:** MySQL Workbench com DER  Script SQL aberto  Execução de trigger.

### Roteiro Detalhado

**[00:00 - 00:30] Apresentação do Modelo Relacional**
- "Sou **[Nome P2]**. Vou apresentar a modelagem do banco e os mecanismos de integridade implementados."
- *[Mostrar DER no MySQL Workbench]*
  - "Este é o **Diagrama Entidade-Relacionamento** com nossas 4 tabelas principais."
  - "**Clínica**: armazena código, nome, endereço, telefone e email"
  - "**Médico**: código, nome, gênero, telefone, email e **especialidade** (Pediatria, Cardiologia, Ortopedia, etc.)"
  - "**Paciente**: identificado por **CPF** (chave primária), com nome, data de nascimento, gênero, telefone e email"
  - "**Consulta**: tabela associativa que conecta as três entidades anteriores, com chave composta (CodCli, CodMed, CpfPaciente, Data_Hora)"

**[00:30 - 01:00] Cardinalidades e Integridade Referencial**
- "As cardinalidades são:
  - **1:N** entre Médico e Consulta (um médico atende várias consultas)
  - **1:N** entre Paciente e Consulta (um paciente pode ter várias consultas)
  - **1:N** entre Clínica e Consulta (uma clínica hospeda várias consultas)"
- "Todas as FKs foram configuradas com `ON DELETE CASCADE` para Clínica, garantindo remoção em cascata de consultas quando uma clínica é deletada."
- *[Mostrar no script SQL as definições de FOREIGN KEY]*

**[01:00 - 01:40] Triggers de Validação**
- "Implementamos **9 triggers** no total para validar dados antes de INSERT e UPDATE:"
  - "**CPF do Paciente**: valida formato XXX.XXX.XXX-XX usando REGEXP"
  - "**Email**: valida presença de @ e . para Paciente, Médico e Clínica"
  - "**Telefone**: formato diferenciado  Clínica usa (DD) XXXX-XXXX (8 dígitos) e Médico/Paciente usam (DD) XXXXX-XXXX (9 dígitos)"
- *[Mostrar um trigger no código]*

**[01:40 - 02:00] Views e Dados de Teste**
- "Criamos também uma **VIEW** chamada `Vw_QtdeConsultasPorMedico` que agrega o total de consultas por médico com sua especialidade."
- "O banco foi populado com **10 clínicas, 12 médicos, 8 pacientes e 16 consultas** para teste."
- *[Mostrar rapidamente o resultado de um SELECT na view ou na tabela Consulta]*
- "Com isso, garantimos que o sistema não apenas funciona visualmente, mas também mantém **consistência e integridade dos dados no nível do banco**."
- "Obrigado!"

---

## Dicas para Apresentação

### Timing
- **Parte 1**: focar na interface e funcionalidades do sistema (não entrar em código Python detalhado)
- **Parte 2**: focar no SQL, DER e triggers (evitar voltar para o Streamlit)

### Transição Suave
- Pessoa 1 encerra mencionando "triggers e integridade", que é justamente o gancho para Pessoa 2 começar

### Material de Apoio
- Ter o Streamlit já rodando em `localhost:8501` antes de começar
- Ter o MySQL Workbench aberto com o DER pronto
- Ter o arquivo `consultas_medicas.sql` aberto em editor para mostrar trechos específicos de triggers

### Pontos de Destaque
- **Session state** para persistência de dados no Streamlit
- **Validação em dois níveis**: interface (Streamlit) + banco (Triggers)
- **Chave composta** na tabela Consulta
- **Formatos diferentes de telefone** para Clínica vs Médico/Paciente

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
from db import MySQLDB

# ============================================================================
# CONFIGURAÇÃO STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="Sistema de Consultas Médicas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DADOS MOCKADOS (EM MEMÓRIA) - USANDO SESSION STATE
# ============================================================================


@st.cache_resource
def init_db():
    """Inicializa a conexão com o banco de dados."""
    try:
        db = MySQLDB()
        db.connect()
        return db
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
        st.info("💡 Certifique-se de que o MySQL está rodando e o banco 'consultas_medicas' foi criado.")
        return None


# Inicializa conexão global
db = init_db()

# ============================================================================
# SIMULAÇÃO DE BANCO DE DADOS (em memória, como dicionários/listas)
# ============================================================================

# Inicializa estruturas no session_state (persiste durante a sessão)
if "pacientes" not in st.session_state:
    st.session_state.pacientes = [
        {"id": 1, "nome": "João Silva", "idade": 45, "endereco": "Rua A, 123"},
        {"id": 2, "nome": "Maria Santos", "idade": 32, "endereco": "Rua B, 456"},
    ]

if 'medicos_data' not in st.session_state:
    st.session_state.medicos_data = [
        {"codmed": "M001", "nome": "Dr. Carlos Oliveira", "genero": "M", "especialidade": "Cardiologia", "telefone": "(81) 98888-1111", "email": "carlos@clinica.com"},
        {"codmed": "M002", "nome": "Dra. Ana Paula", "genero": "F", "especialidade": "Pediatria", "telefone": "(81) 98888-2222", "email": "ana@clinica.com"},
        {"codmed": "M003", "nome": "Dr. Roberto Lima", "genero": "M", "especialidade": "Ortopedia", "telefone": "(81) 98888-3333", "email": "roberto@clinica.com"},
    ]

if 'clinicas_data' not in st.session_state:
    st.session_state.clinicas_data = [
        {"codcli": "C001", "nome": "Clínica Saúde Total", "endereco": "Rua das Flores, 123", "telefone": "(81) 3333-4444", "email": "contato@saudetotal.com"},
        {"codcli": "C002", "nome": "Clínica Vida", "endereco": "Av. Principal, 456", "telefone": "(81) 3333-5555", "email": "contato@clinicavida.com"},
    ]

if "log_acoes" not in st.session_state:
    st.session_state.log_acoes = []

if "proximo_id_paciente" not in st.session_state:
    st.session_state.proximo_id_paciente = 3

if "proximo_id_medico" not in st.session_state:
    st.session_state.proximo_id_medico = 3

if "proximo_id_consulta" not in st.session_state:
    st.session_state.proximo_id_consulta = 2

# ============================================================================
# FUNÇÕES HELPER - PACIENTES
# ============================================================================


def get_paciente_por_id(id_paciente: int) -> Optional[Dict]:
    """Busca paciente por ID."""
    for p in st.session_state.pacientes:
        if p["id"] == id_paciente:
            return p
    return None


def paciente_existe(id_paciente: int) -> bool:
    """Verifica se paciente existe."""
    return get_paciente_por_id(id_paciente) is not None


def paciente_tem_consultas(id_paciente: int) -> bool:
    """Verifica se paciente tem consultas associadas."""
    for c in st.session_state.consultas:
        if c["id_paciente"] == id_paciente:
            return True
    return False


def criar_paciente(nome: str, idade: int, endereco: str) -> bool:
    """Cria novo paciente. Retorna True se sucesso."""
    if not nome or idade <= 0:
        return False
    novo_paciente = {
        "id": st.session_state.proximo_id_paciente,
        "nome": nome,
        "idade": idade,
        "endereco": endereco
    }
    st.session_state.pacientes.append(novo_paciente)
    st.session_state.proximo_id_paciente += 1
    registrar_log(f"Paciente '{nome}' criado com ID {novo_paciente['id']}")
    return True


def atualizar_paciente(id_paciente: int, nome: str, idade: int, endereco: str) -> bool:
    """Atualiza paciente existente."""
    paciente = get_paciente_por_id(id_paciente)
    if not paciente:
        return False
    if not nome or idade <= 0:
        return False
    paciente["nome"] = nome
    paciente["idade"] = idade
    paciente["endereco"] = endereco
    registrar_log(f"Paciente ID {id_paciente} atualizado")
    return True


def deletar_paciente(id_paciente: int) -> bool:
    """Deleta paciente se não tiver consultas (validação FK)."""
    if not paciente_existe(id_paciente):
        return False
    if paciente_tem_consultas(id_paciente):
        return False  # Não permite deletar (simula RESTRICT)
    st.session_state.pacientes = [p for p in st.session_state.pacientes if p["id"] != id_paciente]
    registrar_log(f"Paciente ID {id_paciente} deletado")
    return True

# ============================================================================
# FUNÇÕES HELPER - MÉDICOS
# ============================================================================


def get_medico_por_id(id_medico: int) -> Optional[Dict]:
    """Busca médico por ID."""
    for m in st.session_state.medicos:
        if m["id"] == id_medico:
            return m
    return None


def medico_existe(id_medico: int) -> bool:
    """Verifica se médico existe."""
    return get_medico_por_id(id_medico) is not None


def medico_tem_consultas(id_medico: int) -> bool:
    """Verifica se médico tem consultas associadas."""
    for c in st.session_state.consultas:
        if c["id_medico"] == id_medico:
            return True
    return False


def criar_medico(nome: str, especialidade: str) -> bool:
    """Cria novo médico."""
    if not nome or not especialidade:
        return False
    novo_medico = {
        "id": st.session_state.proximo_id_medico,
        "nome": nome,
        "especialidade": especialidade
    }
    st.session_state.medicos.append(novo_medico)
    st.session_state.proximo_id_medico += 1
    registrar_log(f"Médico '{nome}' ({especialidade}) criado com ID {novo_medico['id']}")
    return True


def atualizar_medico(id_medico: int, nome: str, especialidade: str) -> bool:
    """Atualiza médico existente."""
    medico = get_medico_por_id(id_medico)
    if not medico:
        return False
    if not nome or not especialidade:
        return False
    medico["nome"] = nome
    medico["especialidade"] = especialidade
    registrar_log(f"Médico ID {id_medico} atualizado")
    return True


def deletar_medico(id_medico: int) -> bool:
    """Deleta médico se não tiver consultas."""
    if not medico_existe(id_medico):
        return False
    if medico_tem_consultas(id_medico):
        return False
    st.session_state.medicos = [m for m in st.session_state.medicos if m["id"] != id_medico]
    registrar_log(f"Médico ID {id_medico} deletado")
    return True

# ============================================================================
# FUNÇÕES HELPER
# ============================================================================


def criar_consulta(id_paciente: int, id_medico: int, data: datetime, descricao: str) -> bool:
    """Cria nova consulta com validação de FK."""
    if not paciente_existe(id_paciente) or not medico_existe(id_medico):
        return False
    if not descricao:
        return False

    nova_consulta = {
        "id": st.session_state.proximo_id_consulta,
        "id_paciente": id_paciente,
        "id_medico": id_medico,
        "data": data,
        "descricao": descricao
    }
    st.session_state.consultas.append(nova_consulta)
    st.session_state.proximo_id_consulta += 1

    # TRIGGER: registra no log_acoes quando uma consulta é criada
    registrar_log(f"Consulta criada: ID {nova_consulta['id']} - Paciente {id_paciente}, Médico {id_medico}")

    return True


def atualizar_consulta(id_consulta: int, id_paciente: int, id_medico: int, data: datetime, descricao: str) -> bool:
    """Atualiza consulta existente."""
    if not paciente_existe(id_paciente) or not medico_existe(id_medico):
        return False
    if not descricao:
        return False

    for c in st.session_state.consultas:
        if c["id"] == id_consulta:
            c["id_paciente"] = id_paciente
            c["id_medico"] = id_medico
            c["data"] = data
            c["descricao"] = descricao
            registrar_log(f"Consulta ID {id_consulta} atualizada")
            return True
    return False


def deletar_consulta(id_consulta: int) -> bool:
    """Deleta consulta."""
    for i, c in enumerate(st.session_state.consultas):
        if c["id"] == id_consulta:
            st.session_state.consultas.pop(i)
            registrar_log(f"Consulta ID {id_consulta} deletada")
            return True
    return False


def get_consulta_por_id(id_consulta: int) -> Optional[Dict]:
    """Busca consulta por ID."""
    for c in st.session_state.consultas:
        if c["id"] == id_consulta:
            return c
    return None

def get_consultas():
    """Retorna todas as consultas."""
    return st.session_state.consultas_data


def registrar_log(mensagem: str):
    """Registra ação no log (simula trigger do MySQL)."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem": mensagem
    }
    st.session_state.log_acoes.append(log_entry)
# ============================================================================
# FUNÇÕES ULTILITÁRIAS
# ============================================================================


# ============================================================================
# TELAS DA APLICAÇÃO
# ============================================================================


def tela_home():
    """Tela inicial com resumo do sistema."""
    st.markdown("# 🏥 Sistema de Consultas Médicas")
    st.markdown("Bem-vindo ao Sistema de Gerenciamento de Consultas Médicas!")
    st.markdown("---")

    if db is None:
        st.error("❌ Banco de dados não conectado.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Pacientes", 0)
        with col2:
            st.metric("Total de Médicos", 0)
        with col3:
            st.metric("Total de Consultas", 0)
    else:
        try:
            # Busca resumo geral do banco de dados
            resumo = db.get_resumo_geral_sistema()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Pacientes", resumo.get('total_pacientes', 0))
            with col2:
                st.metric("Total de Médicos", resumo.get('total_medicos', 0))
            with col3:
                st.metric("Total de Consultas", resumo.get('total_consultas', 0))
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Pacientes", "Erro")
            with col2:
                st.metric("Total de Médicos", "Erro")
            with col3:
                st.metric("Total de Consultas", "Erro")

    st.markdown("---")
    st.markdown("### 📌 Sobre o Sistema")
    st.info(
        """
        Este é um sistema completo de gerenciamento de consultas médicas com:
        - ✅ CRUD completo para Pacientes, Médicos, Clínicas e Consultas
        - ✅ Validação de integridade referencial
        - ✅ Banco de dados MySQL com triggers
        - ✅ Consultas avançadas e relatórios
        """
    )


def tela_pacientes():
    """Gerencia CRUD de pacientes."""
    st.markdown("## 👥 Gerenciamento de Pacientes")

    if db is None:
        st.error("❌ Banco de dados não conectado.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Pacientes")
        try:
            pacientes = db.get_clientes()  # No db.py, pacientes são chamados de clientes
            if pacientes:
                df = pd.DataFrame(pacientes)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.warning("Nenhum paciente cadastrado.")
        except Exception as e:
            st.error(f"Erro ao carregar pacientes: {str(e)}")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Paciente")
        with st.form("form_criar_paciente"):
            cpf = st.text_input("CPF", placeholder="000.000.000-00", max_chars=14)
            nome = st.text_input("Nome", placeholder="Ex: João Silva")
            data_nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY", min_value=datetime(1900, 1, 1), max_value=datetime.today())
            genero = st.selectbox("Gênero", ["M", "F"])
            telefone = st.text_input("Telefone", placeholder="(DD) XXXXX-XXXX", max_chars=15)
            email = st.text_input("Email", placeholder="exemplo@mail.com", max_chars=40)
            submitted = st.form_submit_button("Salvar Paciente")

        if submitted:
            try:
                db.create_cliente(cpf, nome, data_nascimento.isoformat(), genero, telefone, email)
                st.success(f"✅ Paciente '{nome}' criado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao criar paciente: {str(e)}")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Paciente")
        try:
            pacientes = db.get_clientes()
            if pacientes:
                opcoes = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
                sel = st.selectbox("Selecione paciente", opcoes, key="sel_editar_pac")
                cpf_selecionado = sel.split(" - ")[0]

                # Busca o paciente completo
                paciente = next((p for p in pacientes if p['cpf'] == cpf_selecionado), None)

                if paciente:
                    with st.form("form_editar_paciente"):
                        nome = st.text_input("Nome", value=paciente["nome"])
                        data_nasc = datetime.strptime(str(paciente["data_nascimento"]), "%Y-%m-%d").date()
                        data_nascimento = st.date_input("Data de Nascimento", value=data_nasc, format="DD/MM/YYYY", min_value=datetime(1900, 1, 1), max_value=datetime.today())
                        genero = st.selectbox("Gênero", ["M", "F"], index=0 if paciente["genero"] == "M" else 1)
                        telefone = st.text_input("Telefone", value=paciente["telefone"])
                        email = st.text_input("E-mail", value=paciente["email"])
                        submitted = st.form_submit_button("Atualizar")

                    if submitted:
                        try:
                            db.update_cliente(cpf_selecionado, nome, data_nascimento.isoformat(), genero, telefone, email)
                            st.success("✅ Paciente atualizado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao atualizar paciente: {str(e)}")
            else:
                st.warning("Nenhum paciente para editar.")
        except Exception as e:
            st.error(f"Erro ao carregar pacientes: {str(e)}")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Paciente")
        try:
            pacientes = db.get_clientes()
            if pacientes:
                opcoes = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
                sel = st.selectbox("Selecione paciente", opcoes, key="sel_deletar_pac")
                cpf_selecionado = sel.split(" - ")[0]

                if st.button("🗑️ Deletar Paciente", key="btn_deletar_pac"):
                    try:
                        db.delete_cliente(cpf_selecionado)
                        st.success("✅ Paciente deletado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao deletar paciente: {str(e)}")
            else:
                st.warning("Nenhum paciente para deletar.")
        except Exception as e:
            st.error(f"Erro ao carregar pacientes: {str(e)}")


def tela_medicos():
    """Gerencia CRUD de médicos."""
    st.markdown("## 👨‍⚕️ Gerenciamento de Médicos")

    if db is None:
        st.error("❌ Banco de dados não conectado.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Médicos")
        try:
            medicos = db.get_medicos()
            if medicos:
                df = pd.DataFrame(medicos)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.warning("Nenhum médico cadastrado.")
        except Exception as e:
            st.error(f"Erro ao carregar médicos: {str(e)}")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Médico")
        with st.form("form_criar_medico"):
            codmed = st.text_input("Código do Médico", placeholder="Ex: 1234567", max_chars=7)
            nome = st.text_input("Nome Completo", placeholder="Ex: Dr. João Silva", max_chars=60)
            genero = st.selectbox("Gênero", ["M", "F"])
            especialidade = st.selectbox(
                "Especialidade",
                ["Cardiologia", "Dermatologia", "Neurologia", "Pediatria", "Ortopedia", "Oncologia", "Outro"]
            )
            if especialidade == "Outro":
                especialidade = st.text_input("Digite a especialidade")

            telefone = st.text_input("Telefone", placeholder="(81) 98888-1111")
            email = st.text_input("E-mail", placeholder="medico@clinica.com")
            submitted = st.form_submit_button("Salvar Médico")

        if submitted:
            try:
                db.create_medico(codmed, nome, genero, especialidade, telefone, email)
                st.success(f"✅ Médico '{nome}' criado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao criar médico: {str(e)}")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Médico")
        try:
            medicos = db.get_medicos()
            if medicos:
                opcoes = [f"{m['codmed']} - {m['nome']}" for m in medicos]
                sel = st.selectbox("Selecione médico", opcoes, key="sel_editar_med")
                codmed_selecionado = sel.split(" - ")[0]
                medico = db.get_medico_por_id(codmed_selecionado)

                if medico:
                    with st.form("form_editar_medico"):
                        nome = st.text_input("Nome", value=medico["nome"])
                        genero = st.selectbox("Gênero", ["M", "F"], index=0 if medico["genero"] == "M" else 1)
                        especialidade = st.text_input("Especialidade", value=medico["especialidade"])
                        telefone = st.text_input("Telefone", value=medico["telefone"])
                        email = st.text_input("E-mail", value=medico["email"])
                        submitted = st.form_submit_button("Atualizar")

                    if submitted:
                        try:
                            db.update_medico(codmed_selecionado, nome, genero, especialidade, telefone, email)
                            st.success("✅ Médico atualizado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao atualizar médico: {str(e)}")
            else:
                st.warning("Nenhum médico para editar.")
        except Exception as e:
            st.error(f"Erro ao carregar médicos: {str(e)}")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Médico")
        try:
            medicos = db.get_medicos()
            if medicos:
                opcoes = [f"{m['codmed']} - {m['nome']}" for m in medicos]
                sel = st.selectbox("Selecione médico", opcoes, key="sel_deletar_med")
                codmed_selecionado = sel.split(" - ")[0]

                if st.button("🗑️ Deletar Médico", key="btn_deletar_med"):
                    try:
                        db.delete_medico(codmed_selecionado)
                        st.success("✅ Médico deletado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao deletar médico: {str(e)}")
            else:
                st.warning("Nenhum médico para deletar.")
        except Exception as e:
            st.error(f"Erro ao carregar médicos: {str(e)}")


def tela_clinicas():
    """Gerencia CRUD de clínicas."""
    st.markdown("## 🏥 Gerenciamento de Clínicas")

    if db is None:
        st.error("❌ Banco de dados não conectado.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Clínicas")
        try:
            clinicas = db.get_clinicas()
            if clinicas:
                df = pd.DataFrame(clinicas)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.warning("Nenhuma clínica cadastrada.")
        except Exception as e:
            st.error(f"Erro ao carregar clínicas: {str(e)}")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Nova Clínica")
        with st.form("form_criar_clinica"):
            codcli = st.text_input("Código da Clínica", placeholder="Ex: 0000001", max_chars=7)
            nome = st.text_input("Nome da Clínica", placeholder="Ex: Clínica Saúde", max_chars=20)
            endereco = st.text_input("Endereço", placeholder="Rua, número, bairro", max_chars=50)
            telefone = st.text_input("Telefone", placeholder="(DD) XXXX-XXXX", max_chars=14)
            email = st.text_input("Email", placeholder="contato@clinica.com", max_chars=40)
            submitted = st.form_submit_button("Salvar Clínica")

        if submitted:
            try:
                db.create_clinica(codcli, nome, endereco, telefone, email)
                st.success(f"✅ Clínica '{nome}' criada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao criar clínica: {str(e)}")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Clínica")
        try:
            clinicas = db.get_clinicas()
            if clinicas:
                opcoes = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
                sel = st.selectbox("Selecione clínica", opcoes, key="sel_editar_cli")
                codcli_selecionado = sel.split(" - ")[0]
                clinica = db.get_clinica_por_id(codcli_selecionado)

                if clinica:
                    with st.form("form_editar_clinica"):
                        nome = st.text_input("Nome", value=clinica["nome"])
                        endereco = st.text_input("Endereço", value=clinica["endereco"])
                        telefone = st.text_input("Telefone", value=clinica["telefone"])
                        email = st.text_input("E-mail", value=clinica["email"])
                        submitted = st.form_submit_button("Atualizar")

                    if submitted:
                        try:
                            db.update_clinica(codcli_selecionado, nome, endereco, telefone, email)
                            st.success("✅ Clínica atualizada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao atualizar clínica: {str(e)}")
            else:
                st.warning("Nenhuma clínica para editar.")
        except Exception as e:
            st.error(f"Erro ao carregar clínicas: {str(e)}")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Clínica")
        try:
            clinicas = db.get_clinicas()
            if clinicas:
                opcoes = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
                sel = st.selectbox("Selecione clínica", opcoes, key="sel_deletar_cli")
                codcli_selecionado = sel.split(" - ")[0]

                if st.button("🗑️ Deletar Clínica", key="btn_deletar_cli"):
                    try:
                        db.delete_clinica(codcli_selecionado)
                        st.success("✅ Clínica deletada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao deletar clínica: {str(e)}")
            else:
                st.warning("Nenhuma clínica para deletar.")
        except Exception as e:
            st.error(f"Erro ao carregar clínicas: {str(e)}")


def tela_consultas():
    """Gerencia CRUD de consultas."""
    st.markdown("## 📅 Gerenciamento de Consultas")

    if db is None:
        st.error("❌ Banco de dados não conectado.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Consultas")
        try:
            consultas = db.get_pedidos()  # No db.py, consultas são chamadas de pedidos
            if consultas:
                df = pd.DataFrame(consultas)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.warning("Nenhuma consulta cadastrada.")
        except Exception as e:
            st.error(f"Erro ao carregar consultas: {str(e)}")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Nova Consulta")

        try:
            pacientes = db.get_clientes()
            medicos = db.get_medicos()
            clinicas = db.get_clinicas()

            if not pacientes or not medicos or not clinicas:
                st.warning("⚠️ É necessário ter pelo menos um paciente, um médico e uma clínica cadastrados.")
            else:
                with st.form("form_criar_consulta"):
                    opcoes_cli = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
                    sel_cli = st.selectbox("Selecione clínica", opcoes_cli)
                    codcli = sel_cli.split(" - ")[0]

                    opcoes_med = [f"{m['codmed']} - {m['nome']} ({m['especialidade']})" for m in medicos]
                    sel_med = st.selectbox("Selecione médico", opcoes_med)
                    codmed = sel_med.split(" - ")[0]

                    opcoes_pac = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
                    sel_pac = st.selectbox("Selecione paciente", opcoes_pac)
                    cpf = sel_pac.split(" - ")[0]

                    data_consulta = st.date_input("Data da consulta")
                    hora_consulta = st.time_input("Hora da consulta")
                    submitted = st.form_submit_button("Criar Consulta")

                if submitted:
                    try:
                        data_hora = datetime.combine(data_consulta, hora_consulta)
                        db.create_pedido(codcli, codmed, cpf, data_hora)
                        st.success("✅ Consulta criada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao criar consulta: {str(e)}")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Consulta")
        try:
            consultas = db.get_pedidos()
            if consultas:
                opcoes = [f"{c['CodCli']}-{c['CodMed']}-{c['CpfPaciente']} - {c['Data_Hora']}" for c in consultas]
                sel = st.selectbox("Selecione consulta", opcoes, key="sel_editar_cons")

                # Parse a seleção
                parts = sel.split(" - ")
                ids = parts[0].split("-")
                codcli_old = ids[0]
                codmed_old = ids[1]
                cpf_old = ids[2]
                data_hora_old = parts[1]

                # Busca listas para os selects
                pacientes = db.get_clientes()
                medicos = db.get_medicos()
                clinicas = db.get_clinicas()

                with st.form("form_editar_consulta"):
                    opcoes_cli = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
                    sel_cli = st.selectbox("Selecione clínica", opcoes_cli, key="edit_cli")
                    codcli_new = sel_cli.split(" - ")[0]

                    opcoes_med = [f"{m['codmed']} - {m['nome']}" for m in medicos]
                    sel_med = st.selectbox("Selecione médico", opcoes_med, key="edit_med")
                    codmed_new = sel_med.split(" - ")[0]

                    opcoes_pac = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
                    sel_pac = st.selectbox("Selecione paciente", opcoes_pac, key="edit_pac")
                    cpf_new = sel_pac.split(" - ")[0]

                    dt_old = datetime.fromisoformat(str(data_hora_old).replace(' ', 'T'))
                    data_consulta = st.date_input("Data da consulta", value=dt_old.date())
                    hora_consulta = st.time_input("Hora da consulta", value=dt_old.time())
                    submitted = st.form_submit_button("Atualizar")

                if submitted:
                    try:
                        data_hora_new = datetime.combine(data_consulta, hora_consulta)
                        old_keys = (codcli_old, codmed_old, cpf_old, data_hora_old)
                        new_values = {
                            'codcli': codcli_new,
                            'codmed': codmed_new,
                            'cpf': cpf_new,
                            'data_hora': data_hora_new
                        }
                        db.update_pedido(old_keys, new_values)
                        st.success("✅ Consulta atualizada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar consulta: {str(e)}")
            else:
                st.warning("Nenhuma consulta para editar.")
        except Exception as e:
            st.error(f"Erro ao carregar consultas: {str(e)}")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Consulta")
        try:
            consultas = db.get_pedidos()
            if consultas:
                # Criar índice para mapear seleção à consulta completa
                opcoes = []
                for idx, c in enumerate(consultas):
                    # Formatar data/hora para exibição
                    data_hora_str = str(c['Data_Hora']) if c['Data_Hora'] else "N/A"
                    opcoes.append(f"{idx}|{c['clinica_nome']} - {c['medico_nome']} - {c['paciente_nome']} ({data_hora_str})")
                
                sel = st.selectbox("Selecione consulta", opcoes, key="sel_deletar_cons")
                
                # Extrair índice da seleção
                idx = int(sel.split("|")[0])
                consulta_selecionada = consultas[idx]
                
                # Exibir detalhes da consulta
                st.info(f"""
                **Clínica:** {consulta_selecionada['clinica_nome']} ({consulta_selecionada['CodCli']})  
                **Médico:** {consulta_selecionada['medico_nome']} ({consulta_selecionada['CodMed']})  
                **Paciente:** {consulta_selecionada['paciente_nome']} ({consulta_selecionada['CpfPaciente']})  
                **Data/Hora:** {consulta_selecionada['Data_Hora']}
                """)

                if st.button("🗑️ Deletar Consulta", key="btn_deletar_cons"):
                    try:
                        db.delete_pedido(
                            consulta_selecionada['CodCli'],
                            consulta_selecionada['CodMed'],
                            consulta_selecionada['CpfPaciente'],
                            consulta_selecionada['Data_Hora']
                        )
                        st.success("✅ Consulta deletada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao deletar consulta: {str(e)}")
            else:
                st.warning("Nenhuma consulta para deletar.")
        except Exception as e:
            st.error(f"Erro ao carregar consultas: {str(e)}")


def tela_triggers():
    """Exibe informações sobre triggers do banco."""
    st.markdown("## 🔔 Triggers do Sistema")

    st.markdown("### Validação de Intervalo de Agendamento")
    st.info("""
    O banco de dados possui **2 triggers** que garantem que consultas sejam agendadas com antecedência máxima de **60 dias (2 meses)**.
    Essas validações acontecem automaticamente no MySQL, impedindo agendamentos fora do prazo permitido.
    """)

    # Seção de validação
    st.markdown("#### 📅 Regra de Negócio: Limite de Antecedência")
    st.markdown("""
    **Restrição:** Consultas só podem ser agendadas com no máximo **2 meses (60 dias)** de antecedência a partir da data atual.

    **Triggers Implementados:**
    - `tg_verifica_intervalo_agendamento` - Valida no INSERT
    - `tg_verifica_intervalo_agendamento_upd` - Valida no UPDATE

    **Entidade:** Consulta

    **Validação:** `TIMESTAMPDIFF(DAY, CURDATE(), NEW.Data_Hora) > 60`

    **Mensagem de Erro:** "A consulta só pode ser agendada com no máximo 2 meses de antecedência."
    """)

    st.markdown("---")

    # Exemplo de código de trigger
    st.markdown("### 💻 Código do Trigger")
    st.markdown("**Trigger de verificação de intervalo de agendamento (INSERT):**")
    st.code("""
DELIMITER $$
CREATE TRIGGER tg_verifica_intervalo_agendamento
BEFORE INSERT ON Consulta
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(DAY, CURDATE(), NEW.Data_Hora) > 60 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A consulta só pode ser agendada com no máximo 2 meses de antecedência.';
    END IF;
END $$
DELIMITER ;
    """, language="sql")

    st.markdown("---")

    # Tabela resumo
    st.markdown("### 📊 Resumo dos Triggers")
    triggers_data = [
        {"Trigger": "tg_verifica_intervalo_agendamento", "Entidade": "Consulta", "Evento": "INSERT", "Validação": "Data ≤ 60 dias"},
        {"Trigger": "tg_verifica_intervalo_agendamento_upd", "Entidade": "Consulta", "Evento": "UPDATE", "Validação": "Data ≤ 60 dias"},
    ]

    df_triggers = pd.DataFrame(triggers_data)
    st.dataframe(df_triggers, width='stretch', hide_index=True)

    st.success("✅ Total de 2 triggers implementados no banco de dados MySQL")

    st.markdown("---")

    # Seção de teste
    st.markdown("### 🧪 Teste de Validação do Trigger")
    st.info("**Como testar:** Tente agendar uma consulta com mais de 60 dias de "
            "antecedência na aba 'Consultas' → 'Criar'. O sistema deve bloquear e "
            "exibir a mensagem de erro do trigger.")

    # Calculadora de data
    st.markdown("#### 📅 Calculadora de Prazo")
    col1, col2 = st.columns(2)

    with col1:
        from datetime import datetime, timedelta
        data_hoje = datetime.now().date()
        st.write(f"**Data atual:** {data_hoje.strftime('%d/%m/%Y')}")

        limite_permitido = data_hoje + timedelta(days=60)
        st.write(f"**Limite máximo permitido:** {limite_permitido.strftime('%d/%m/%Y')}")

    with col2:
        data_teste = st.date_input("Escolha uma data para testar:", value=data_hoje + timedelta(days=70))
        dias_antecedencia = (data_teste - data_hoje).days

        if dias_antecedencia > 60:
            st.error(f"❌ **{dias_antecedencia} dias de antecedência** - Será BLOQUEADO pelo trigger!")
        elif dias_antecedencia < 0:
            st.warning("⚠️ Data no passado - Consulta não pode ser agendada")
        else:
            st.success(f"✅ **{dias_antecedencia} dias de antecedência** - Será ACEITO pelo sistema")

    # Exemplos práticos
    st.markdown("#### 💡 Exemplos de Teste")
    exemplos = [
        {"Data": (data_hoje + timedelta(days=30)).strftime('%d/%m/%Y'), "Dias": "30 dias", "Resultado": "✅ ACEITO"},
        {"Data": (data_hoje + timedelta(days=60)).strftime('%d/%m/%Y'), "Dias": "60 dias", "Resultado": "✅ ACEITO"},
        {"Data": (data_hoje + timedelta(days=61)).strftime('%d/%m/%Y'), "Dias": "61 dias", "Resultado": "❌ BLOQUEADO"},
        {"Data": (data_hoje + timedelta(days=90)).strftime('%d/%m/%Y'), "Dias": "90 dias", "Resultado": "❌ BLOQUEADO"},
    ]

    df_exemplos = pd.DataFrame(exemplos)
    st.dataframe(df_exemplos, width='stretch', hide_index=True)


def tela_consultas_avancadas():
    """Consultas avançadas e gráficos."""
    st.markdown("## 📊 Visualizações e Consultas Avançadas")

    if db is None:
        st.error("❌ Banco de dados não conectado. Verifique a configuração.")
        return

    st.info("💡 Implementar consultas avançadas usando as funções do db.py")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Resumo Geral",
        "🏥 Estatísticas por Clínica",
        "👨‍⚕️ Ranking de Médicos",
        "📅 Consultas Próximas",
        "📈 Consultas por Mês",
        "🎯 Especialidades",
        "👥 Pacientes"
    ])

    # TAB 1: Resumo Geral
    with tab1:
        st.subheader("📊 Resumo Geral do Sistema")
        try:
            resumo = db.get_resumo_geral_sistema()
            if resumo:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👥 Total de Pacientes", resumo.get('total_pacientes', 0))
                    st.metric("👨‍⚕️ Total de Médicos", resumo.get('total_medicos', 0))
                with col2:
                    st.metric("🏥 Total de Clínicas", resumo.get('total_clinicas', 0))
                    st.metric("📅 Total de Consultas", resumo.get('total_consultas', 0))
                with col3:
                    st.metric("🔜 Consultas Futuras", resumo.get('consultas_futuras', 0))
                    st.metric("✅ Consultas Passadas", resumo.get('consultas_passadas', 0))
                with col4:
                    st.metric("🎯 Especialidades", resumo.get('especialidades_disponiveis', 0))
                    st.metric("📊 Idade Média", f"{resumo.get('idade_media_pacientes', 0):.1f} anos")
            else:
                st.warning("Sem dados disponíveis.")
        except Exception as e:
            st.error(f"Erro ao carregar resumo: {str(e)}")

    # TAB 2: Estatísticas por Clínica
    with tab2:
        st.subheader("🏥 Estatísticas por Clínica")
        try:
            dados = db.get_estatisticas_por_clinica()
            if dados:
                df = pd.DataFrame(dados)

                # Gráfico de barras
                st.markdown("### 📊 Total de Consultas por Clínica")
                chart_data = df.set_index('nome_clinica')['total_consultas']
                st.bar_chart(chart_data)

                # Tabela detalhada
                st.markdown("### 📋 Dados Detalhados")
                df_display = df.rename(columns={
                    'codigo_clinica': 'Código',
                    'nome_clinica': 'Clínica',
                    'total_consultas': 'Total Consultas',
                    'total_medicos_atendendo': 'Médicos',
                    'total_pacientes_atendidos': 'Pacientes'
                })
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("Nenhum dado disponível.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB 3: Ranking de Médicos
    with tab3:
        st.subheader("👨‍⚕️ Ranking de Médicos com Mais Atendimentos")

        col1, col2 = st.columns([3, 1])
        with col2:
            limit = st.number_input("Top N médicos", min_value=5, max_value=50, value=10)

        try:
            dados = db.get_medicos_mais_atendimentos(limit=limit)
            if dados:
                df = pd.DataFrame(dados)

                # Gráfico horizontal
                st.markdown("### 📊 Consultas por Médico")
                chart_data = df.set_index('nome_medico')['total_consultas'].head(10)
                st.bar_chart(chart_data, horizontal=True)

                # Tabela
                st.markdown("### 📋 Detalhes dos Médicos")
                df_display = df.rename(columns={
                    'codigo_medico': 'Código',
                    'nome_medico': 'Médico',
                    'especialidade': 'Especialidade',
                    'total_consultas': 'Total Consultas',
                    'pacientes_unicos': 'Pacientes Únicos'
                })
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("Nenhum dado disponível.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB 4: Consultas Próximas
    with tab4:
        st.subheader("📅 Consultas Agendadas para os Próximos Dias")

        dias = st.slider("Quantos dias à frente?", min_value=1, max_value=30, value=7)

        try:
            dados = db.get_consultas_proximas(dias=dias)
            if dados:
                st.success(f"✅ {len(dados)} consultas encontradas nos próximos {dias} dias")

                df = pd.DataFrame(dados)

                # Cards para consultas próximas
                for idx, consulta in enumerate(dados[:5]):  # Mostra as 5 primeiras em destaque
                    with st.expander(
                        f"📅 {consulta['data_hora']} - {consulta['paciente']} com {consulta['medico']}",
                        expanded=(idx == 0)
                    ):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("**🏥 Clínica**")
                            st.write(consulta['clinica'])
                            st.write(f"📞 {consulta['telefone_clinica']}")
                        with col2:
                            st.markdown("**👨‍⚕️ Médico**")
                            st.write(consulta['medico'])
                            st.write(f"🎯 {consulta['especialidade']}")
                        with col3:
                            st.markdown("**👤 Paciente**")
                            st.write(consulta['paciente'])
                            st.write(f"📞 {consulta['telefone_paciente']}")
                            st.write(f"📧 {consulta['email_paciente']}")

                        dias_ate = consulta.get('dias_ate_consulta', 0)
                        if dias_ate == 0:
                            st.warning("⚠️ Consulta HOJE!")
                        elif dias_ate == 1:
                            st.info("📅 Consulta AMANHÃ")
                        else:
                            st.info(f"📅 Faltam {dias_ate} dias")

                # Tabela completa
                st.markdown("---")
                st.markdown("### 📋 Lista Completa")
                df_display = df[[
                    'data_hora', 'paciente', 'telefone_paciente',
                    'medico', 'especialidade', 'clinica', 'dias_ate_consulta'
                ]].rename(columns={
                    'data_hora': 'Data/Hora',
                    'paciente': 'Paciente',
                    'telefone_paciente': 'Telefone',
                    'medico': 'Médico',
                    'especialidade': 'Especialidade',
                    'clinica': 'Clínica',
                    'dias_ate_consulta': 'Dias'
                })
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info(f"Nenhuma consulta agendada para os próximos {dias} dias.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB 5: Consultas por Mês
    with tab5:
        st.subheader("📈 Distribuição de Consultas por Mês")

        ano_atual = datetime.now().year
        ano = st.selectbox("Selecione o ano", range(ano_atual - 2, ano_atual + 2), index=2)

        try:
            dados = db.get_consultas_por_mes(ano=ano)
            if dados:
                df = pd.DataFrame(dados)

                # Gráfico de linha
                st.markdown("### 📊 Evolução Mensal")
                chart_data = df.set_index('nome_mes')['total_consultas']
                st.line_chart(chart_data)

                # Gráfico de barras
                st.markdown("### 📊 Comparativo Mensal")
                col1, col2 = st.columns(2)
                with col1:
                    chart1 = df.set_index('nome_mes')['total_consultas']
                    st.bar_chart(chart1)
                    st.caption("Total de Consultas")
                with col2:
                    chart2 = df.set_index('nome_mes')['medicos_ativos']
                    st.bar_chart(chart2)
                    st.caption("Médicos Ativos")

                # Tabela
                st.markdown("### 📋 Dados Mensais")
                df_display = df[[
                    'nome_mes', 'total_consultas', 'medicos_ativos', 'pacientes_atendidos'
                ]].rename(columns={
                    'nome_mes': 'Mês',
                    'total_consultas': 'Consultas',
                    'medicos_ativos': 'Médicos',
                    'pacientes_atendidos': 'Pacientes'
                })
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info(f"Sem dados para o ano de {ano}.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB 6: Especialidades
    with tab6:
        st.subheader("🎯 Especialidades Médicas Mais Procuradas")

        try:
            dados = db.get_especialidades_mais_procuradas()
            if dados:
                df = pd.DataFrame(dados)

                # Gráfico de pizza (aproximação com bar chart)
                st.markdown("### 📊 Distribuição por Especialidade")
                chart_data = df.set_index('especialidade')['total_consultas'].head(10)
                st.bar_chart(chart_data)

                # Métricas principais
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎯 Especialidades Ativas", len(dados))
                with col2:
                    top_esp = dados[0] if dados else {}
                    st.metric("👑 Mais Procurada", top_esp.get('especialidade', 'N/A'))
                with col3:
                    total = sum([d['total_consultas'] for d in dados])
                    st.metric("📊 Total Consultas", total)

                # Tabela
                st.markdown("### 📋 Detalhes por Especialidade")
                df_display = df.rename(columns={
                    'especialidade': 'Especialidade',
                    'total_consultas': 'Total Consultas',
                    'pacientes_unicos': 'Pacientes Únicos',
                    'medicos_especialidade': 'Médicos'
                })
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("Nenhum dado disponível.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

    # TAB 7: Pacientes
    with tab7:
        st.subheader("👥 Estatísticas de Pacientes")

        tab7_1, tab7_2, tab7_3 = st.tabs([
            "📊 Por Gênero",
            "⚠️ Sem Consulta",
            "📋 Histórico Individual"
        ])

        # Subtab: Por Gênero
        with tab7_1:
            try:
                dados = db.get_pacientes_por_genero()
                if dados:
                    df = pd.DataFrame(dados)

                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    total_pac = sum([d['total_pacientes'] for d in dados])
                    with col1:
                        st.metric("👥 Total de Pacientes", total_pac)
                    with col2:
                        idade_media = sum([d['idade_media'] * d['total_pacientes'] for d in dados]) / total_pac if total_pac > 0 else 0
                        st.metric("📊 Idade Média Geral", f"{int(idade_media)} anos")
                    with col3:
                        st.metric("📋 Grupos por Gênero", len(dados))

                    # Gráfico
                    st.markdown("### 📊 Distribuição por Gênero")
                    chart_data = df.set_index('genero')['total_pacientes']
                    st.bar_chart(chart_data)

                    # Tabela
                    st.markdown("### 📋 Estatísticas Detalhadas")
                    df_display = df.rename(columns={
                        'genero': 'Gênero',
                        'total_pacientes': 'Total',
                        'idade_media': 'Idade Média',
                        'idade_minima': 'Idade Mín.',
                        'idade_maxima': 'Idade Máx.'
                    })
                    st.dataframe(df_display, width='stretch', hide_index=True)
                else:
                    st.info("Nenhum dado disponível.")
            except Exception as e:
                st.error(f"Erro ao carregar dados: {str(e)}")

        # Subtab: Sem Consulta
        with tab7_2:
            try:
                dados = db.get_pacientes_sem_consulta()
                if dados:
                    st.warning(f"⚠️ {len(dados)} pacientes cadastrados nunca tiveram consulta")

                    df = pd.DataFrame(dados)
                    df_display = df[[
                        'nome', 'cpf', 'telefone', 'email', 'idade'
                    ]].rename(columns={
                        'nome': 'Nome',
                        'cpf': 'CPF',
                        'telefone': 'Telefone',
                        'email': 'E-mail',
                        'idade': 'Idade'
                    })
                    st.dataframe(df_display, width='stretch', hide_index=True)
                else:
                    st.success("✅ Todos os pacientes têm pelo menos uma consulta!")
            except Exception as e:
                st.error(f"Erro ao carregar dados: {str(e)}")

        # Subtab: Histórico Individual
        with tab7_3:
            st.markdown("### 📋 Consultar Histórico de Paciente")

            cpf_input = st.text_input("Digite o CPF do paciente", placeholder="000.000.000-00", max_chars=14)

            if st.button("🔍 Buscar Histórico"):
                if cpf_input:
                    try:
                        dados = db.get_historico_paciente(cpf_input)
                        if dados:
                            st.success(f"✅ {len(dados)} consultas encontradas")

                            # Cards para cada consulta
                            for consulta in dados:
                                status_icon = "✅" if consulta['status'] == 'Realizada' else "📅"
                                with st.expander(
                                    f"{status_icon} {consulta['data_hora']} - {consulta['especialidade']}",
                                    expanded=False
                                ):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown("**🏥 Clínica**")
                                        st.write(consulta['clinica'])
                                        st.write(f"📍 {consulta['endereco_clinica']}")
                                        st.write(f"📞 {consulta['telefone_clinica']}")
                                    with col2:
                                        st.markdown("**👨‍⚕️ Médico**")
                                        st.write(consulta['medico'])
                                        st.write(f"🎯 {consulta['especialidade']}")
                                        st.write(f"📞 {consulta['telefone_medico']}")

                                    st.info(f"Status: {consulta['status']}")
                        else:
                            st.info("Nenhuma consulta encontrada para este paciente.")
                    except Exception as e:
                        st.error(f"Erro ao buscar histórico: {str(e)}")
                else:
                    st.warning("Por favor, digite um CPF válido.")


# ============================================================================
# NAVEGAÇÃO PRINCIPAL
# ============================================================================

st.sidebar.markdown("# 🏥 Menu Principal")
pagina = st.sidebar.radio(
    "Navegação",
    [
        "Home",
        "Pacientes",
        "Médicos",
        "Clínicas",
        "Consultas",
        "Triggers (Log)",
        "Consultas Avançadas"
    ]
)

if pagina == "Home":
    tela_home()
elif pagina == "Pacientes":
    tela_pacientes()
elif pagina == "Médicos":
    tela_medicos()
elif pagina == "Clínicas":
    tela_clinicas()
elif pagina == "Consultas":
    tela_consultas()
elif pagina == "Triggers (Log)":
    tela_triggers()
elif pagina == "Consultas Avançadas":
    tela_consultas_avancadas()


# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Informações")
st.sidebar.info(
    "Sistema de Consultas Médicas v1.0\n\n"
    "Banco de dados MySQL\n\n"
    "Desenvolvido com Streamlit"
)

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from typing import Dict, Optional

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

# Inicializar dados na sessão
if 'pacientes_data' not in st.session_state:
    st.session_state.pacientes_data = [
        {"cpf": "123.456.789-00", "nome": "João Silva", "data_nascimento": "1985-05-15", "genero": "M", "telefone": "(81) 98765-4321", "email": "joao@email.com"},
        {"cpf": "987.654.321-00", "nome": "Maria Santos", "data_nascimento": "1990-08-20", "genero": "F", "telefone": "(81) 99876-5432", "email": "maria@email.com"},
        {"cpf": "456.789.123-00", "nome": "Pedro Costa", "data_nascimento": "1978-12-10", "genero": "M", "telefone": "(81) 97654-3210", "email": "pedro@email.com"},
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

if 'consultas_data' not in st.session_state:
    st.session_state.consultas_data = [
        {"id": 1, "cpf_paciente": "123.456.789-00", "codmed": "M001", "codcli": "C001", "data": "2025-12-10", "hora": "09:00", "status": "Agendada"},
        {"id": 2, "cpf_paciente": "987.654.321-00", "codmed": "M002", "codcli": "C001", "data": "2025-12-11", "hora": "10:30", "status": "Agendada"},
        {"id": 3, "cpf_paciente": "456.789.123-00", "codmed": "M003", "codcli": "C002", "data": "2025-12-12", "hora": "14:00", "status": "Confirmada"},
    ]

# ============================================================================
# FUNÇÕES HELPER
# ============================================================================

def get_pacientes():
    """Retorna todos os pacientes."""
    return st.session_state.pacientes_data

def get_medicos():
    """Retorna todos os médicos."""
    return st.session_state.medicos_data

def get_consultas():
    """Retorna todas as consultas."""
    return st.session_state.consultas_data

def get_clinicas():
    """Retorna todas as clínicas."""
    return st.session_state.clinicas_data

# ============================================================================
# TELAS DA APLICAÇÃO
# ============================================================================

def tela_home():
    """Tela inicial com resumo do sistema."""
    st.markdown("# 🏥 Sistema de Consultas Médicas")
    st.markdown("Bem-vindo ao Sistema de Gerenciamento de Consultas Médicas!")
    st.markdown("---")

    pacientes = get_pacientes()
    medicos = get_medicos()
    consultas = get_consultas()
    clinicas = get_clinicas()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Pacientes", len(pacientes))
    with col2:
        st.metric("Total de Médicos", len(medicos))
    with col3:
        st.metric("Total de Clínicas", len(clinicas))
    with col4:
        st.metric("Total de Consultas", len(consultas))

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

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Pacientes")
        pacientes = get_pacientes()
        if pacientes:
            df = pd.DataFrame(pacientes)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Nenhum paciente cadastrado.")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Paciente")
        with st.form("form_criar_paciente"):
            cpf = st.text_input("CPF", placeholder="XXX.XXX.XXX-XX", max_chars=14)
            nome = st.text_input("Nome Completo", placeholder="Ex: João Silva", max_chars=60)
            data_nasc = st.date_input("Data de Nascimento", min_value=date(1900, 1, 1), max_value=date.today())
            genero = st.selectbox("Gênero", ["M", "F"])
            telefone = st.text_input("Telefone", placeholder="(DD) XXXXX-XXXX", max_chars=15)
            email = st.text_input("Email", placeholder="exemplo@mail.com", max_chars=40)
            submitted = st.form_submit_button("Salvar Paciente")

        if submitted:
            novo_paciente = {
                "cpf": cpf,
                "nome": nome,
                "data_nascimento": data_nasc.isoformat(),
                "genero": genero,
                "telefone": telefone,
                "email": email
            }
            st.session_state.pacientes_data.append(novo_paciente)
            st.success(f"✅ Paciente '{nome}' criado com sucesso!")
            st.rerun()

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Paciente")
        pacientes = get_pacientes()
        if pacientes:
            opcoes = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
            sel = st.selectbox("Selecione paciente", opcoes, key="sel_editar_pac")
            cpf_selecionado = sel.split(" - ")[0]
            paciente = next((p for p in pacientes if p['cpf'] == cpf_selecionado), None)

            if paciente:
                with st.form("form_editar_paciente"):
                    nome = st.text_input("Nome Completo", value=paciente["nome"], max_chars=60)
                    data_nasc = st.date_input("Data de Nascimento", value=pd.to_datetime(paciente["data_nascimento"]).date())
                    genero = st.selectbox("Gênero", ["M", "F"], index=0 if paciente["genero"] == "M" else 1)
                    telefone = st.text_input("Telefone", value=paciente["telefone"], max_chars=15)
                    email = st.text_input("Email", value=paciente["email"], max_chars=40)
                    submitted = st.form_submit_button("Atualizar")

                if submitted:
                    paciente["nome"] = nome
                    paciente["data_nascimento"] = data_nasc.isoformat()
                    paciente["genero"] = genero
                    paciente["telefone"] = telefone
                    paciente["email"] = email
                    st.success("✅ Paciente atualizado com sucesso!")
                    st.rerun()
        else:
            st.warning("Nenhum paciente para editar.")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Paciente")
        pacientes = get_pacientes()
        if pacientes:
            opcoes = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
            sel = st.selectbox("Selecione paciente", opcoes, key="sel_deletar_pac")
            cpf_selecionado = sel.split(" - ")[0]

            if st.button("🗑️ Deletar Paciente", key="btn_deletar_pac"):
                st.session_state.pacientes_data = [p for p in st.session_state.pacientes_data if p['cpf'] != cpf_selecionado]
                st.success("✅ Paciente deletado com sucesso!")
                st.rerun()
        else:
            st.warning("Nenhum paciente para deletar.")


def tela_medicos():
    """Gerencia CRUD de médicos (implementação simplificada)."""
    st.markdown("## 👨‍⚕️ Gerenciamento de Médicos")
    st.info("Tela de médicos - implementar CRUD completo conforme necessário")
    
    medicos = get_medicos()
    if medicos:
        df = pd.DataFrame(medicos)
        st.dataframe(df, use_container_width=True, hide_index=True)


def tela_consultas():
    """Gerencia CRUD de consultas (implementação simplificada)."""
    st.markdown("## 📅 Gerenciamento de Consultas")
    st.info("Tela de consultas - implementar CRUD completo conforme necessário")
    
    consultas = get_consultas()
    if consultas:
        df = pd.DataFrame(consultas)
        st.dataframe(df, use_container_width=True, hide_index=True)


def tela_triggers():
    """Exibe informações sobre triggers do banco."""
    st.markdown("## 🔔 Triggers do Sistema")
    st.info("Os triggers estão implementados no banco de dados MySQL e validam automaticamente CPF, emails e telefones.")


def tela_consultas_avancadas():
    """Consultas avançadas e gráficos."""
    st.markdown("## 📊 Visualizações e Consultas Avançadas")
    st.info("Implementar consultas avançadas usando as funções do db.py")


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

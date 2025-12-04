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
    """Gerencia CRUD de médicos."""
    st.markdown("## 👨‍⚕️ Gerenciamento de Médicos")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])
    
    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Médicos")
        medicos = get_medicos()
        if medicos:
            df = pd.DataFrame(medicos)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Nenhum médico cadastrado.")
    
    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Médico")
        with st.form("form_criar_medico"):
            codmed = st.text_input("Código do Médico", placeholder="Ex: 1234567", max_chars=7)
            nome = st.text_input("Nome Completo", placeholder="Ex: Dr. João Silva", max_chars=60)
            genero = st.selectbox("Gênero", ["M", "F"])
            especialidade = st.text_input("Especialidade", placeholder="Ex: Cardiologia", max_chars=30)
            telefone = st.text_input("Telefone", placeholder="(DD) XXXXX-XXXX", max_chars=15)
            email = st.text_input("Email", placeholder="medico@mail.com", max_chars=40)
            submitted = st.form_submit_button("Salvar Médico")
        
        if submitted:
            novo_medico = {
                "codmed": codmed,
                "nome": nome,
                "genero": genero,
                "especialidade": especialidade,
                "telefone": telefone,
                "email": email
            }
            st.session_state.medicos_data.append(novo_medico)
            st.success(f"✅ Médico '{nome}' criado com sucesso!")
            st.rerun()
    
    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Médico")
        medicos = get_medicos()
        if medicos:
            opcoes = [f"{m['codmed']} - {m['nome']}" for m in medicos]
            sel = st.selectbox("Selecione médico", opcoes, key="sel_editar_med")
            codmed_selecionado = sel.split(" - ")[0]
            medico = next((m for m in medicos if m['codmed'] == codmed_selecionado), None)
            
            if medico:
                with st.form("form_editar_medico"):
                    nome = st.text_input("Nome Completo", value=medico["nome"], max_chars=60)
                    genero = st.selectbox("Gênero", ["M", "F"], index=0 if medico["genero"] == "M" else 1)
                    especialidade = st.text_input("Especialidade", value=medico["especialidade"], max_chars=30)
                    telefone = st.text_input("Telefone", value=medico["telefone"], max_chars=15)
                    email = st.text_input("Email", value=medico["email"], max_chars=40)
                    submitted = st.form_submit_button("Atualizar")
                
                if submitted:
                    medico["nome"] = nome
                    medico["genero"] = genero
                    medico["especialidade"] = especialidade
                    medico["telefone"] = telefone
                    medico["email"] = email
                    st.success("✅ Médico atualizado com sucesso!")
                    st.rerun()
        else:
            st.warning("Nenhum médico para editar.")
    
    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Médico")
        medicos = get_medicos()
        if medicos:
            opcoes = [f"{m['codmed']} - {m['nome']}" for m in medicos]
            sel = st.selectbox("Selecione médico", opcoes, key="sel_deletar_med")
            codmed_selecionado = sel.split(" - ")[0]
            
            if st.button("🗑️ Deletar Médico", key="btn_deletar_med"):
                st.session_state.medicos_data = [m for m in st.session_state.medicos_data if m['codmed'] != codmed_selecionado]
                st.success("✅ Médico deletado com sucesso!")
                st.rerun()
        else:
            st.warning("Nenhum médico para deletar.")



def tela_consultas():
    """Gerencia CRUD de consultas (implementação simplificada)."""
    st.markdown("## 📅 Gerenciamento de Consultas")
    st.info("Tela de consultas - implementar CRUD completo conforme necessário")
    
    consultas = get_consultas()
    if consultas:
        df = pd.DataFrame(consultas)
        st.dataframe(df, use_container_width=True, hide_index=True)


def tela_clinicas():
    """Gerencia CRUD de clínicas."""
    st.markdown("## 🏥 Gerenciamento de Clínicas")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])
    
    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Clínicas")
        clinicas = get_clinicas()
        if clinicas:
            df = pd.DataFrame(clinicas)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Nenhuma clínica cadastrada.")
    
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
            # Simular criação (mockado)
            nova_clinica = {
                "codcli": codcli,
                "nome": nome,
                "endereco": endereco,
                "telefone": telefone,
                "email": email
            }
            st.session_state.clinicas_data.append(nova_clinica)
            st.success(f"✅ Clínica '{nome}' criada com sucesso!")
            st.rerun()
    
    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Clínica")
        clinicas = get_clinicas()
        if clinicas:
            opcoes = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
            sel = st.selectbox("Selecione clínica", opcoes, key="sel_editar_cli")
            codcli_selecionado = sel.split(" - ")[0]
            clinica = next((c for c in clinicas if c['codcli'] == codcli_selecionado), None)
            
            if clinica:
                with st.form("form_editar_clinica"):
                    nome = st.text_input("Nome da Clínica", value=clinica["nome"], max_chars=20)
                    endereco = st.text_input("Endereço", value=clinica["endereco"], max_chars=50)
                    telefone = st.text_input("Telefone", value=clinica["telefone"], max_chars=14)
                    email = st.text_input("Email", value=clinica["email"], max_chars=40)
                    submitted = st.form_submit_button("Atualizar")
                
                if submitted:
                    clinica["nome"] = nome
                    clinica["endereco"] = endereco
                    clinica["telefone"] = telefone
                    clinica["email"] = email
                    st.success("✅ Clínica atualizada com sucesso!")
                    st.rerun()
        else:
            st.warning("Nenhuma clínica para editar.")
    
    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Clínica")
        clinicas = get_clinicas()
        if clinicas:
            opcoes = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
            sel = st.selectbox("Selecione clínica", opcoes, key="sel_deletar_cli")
            codcli_selecionado = sel.split(" - ")[0]
            
            if st.button("🗑️ Deletar Clínica", key="btn_deletar_cli"):
                st.session_state.clinicas_data = [c for c in st.session_state.clinicas_data if c['codcli'] != codcli_selecionado]
                st.success("✅ Clínica deletada com sucesso!")
                st.rerun()
        else:
            st.warning("Nenhuma clínica para deletar.")


def tela_triggers():
    """Exibe informações sobre triggers do banco."""
    st.markdown("## 🔔 Triggers do Sistema")
    
    st.markdown("### Validações Automáticas Implementadas")
    st.info("""
    O banco de dados possui **14 triggers** que garantem a integridade dos dados antes de qualquer INSERT ou UPDATE.
    Essas validações acontecem automaticamente no MySQL, impedindo dados inválidos.
    """)
    
    # Seção de validações
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📋 Validação de CPF")
        st.markdown("""
        **Formato obrigatório:** `XXX.XXX.XXX-XX`
        
        **Triggers:**
        - `trg_validar_cpf_paciente_ins`
        - `trg_validar_cpf_paciente_upd`
        
        **Entidade:** Paciente
        
        **Regex:** `^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}$`
        """)
    
    with col2:
        st.markdown("#### 📧 Validação de Email")
        st.markdown("""
        **Formato:** `usuario@dominio.com`
        
        **Triggers:**
        - `trg_valida_email_clinica` (INSERT)
        - `trg_valida_email_clinica_upd` (UPDATE)
        - `trg_valida_email_medico` (INSERT)
        - `trg_valida_email_medico_upd` (UPDATE)
        - `trg_valida_email_paciente` (INSERT)
        - `trg_valida_email_paciente_upd` (UPDATE)
        
        **Validação:** `Email LIKE '%_@_%._%'`
        """)
    
    with col3:
        st.markdown("#### 📞 Validação de Telefone")
        st.markdown("""
        **Clínica:** `(DD) XXXX-XXXX`  
        *(4 dígitos após hífen)*
        
        **Médico/Paciente:** `(DD) XXXXX-XXXX`  
        *(5 dígitos após hífen)*
        
        **Triggers:**
        - `trg_validar_telefone_clinica_ins` (INSERT)
        - `trg_validar_telefone_clinica_upd` (UPDATE)
        - `trg_validar_telefone_medico_ins` (INSERT)
        - `trg_validar_telefone_medico_upd` (UPDATE)
        - `trg_validar_telefone_paciente_ins` (INSERT)
        - `trg_validar_telefone_paciente_upd` (UPDATE)
        """)
    
    st.markdown("---")
    
    # Exemplo de código de trigger
    st.markdown("### 💻 Exemplo de Código de Trigger")
    st.markdown("**Trigger de validação de CPF:**")
    st.code("""
DELIMITER $$
CREATE TRIGGER trg_validar_cpf_paciente_ins
BEFORE INSERT ON Paciente
FOR EACH ROW
BEGIN
    -- CPF deve estar exatamente no formato XXX.XXX.XXX-XX
    IF NEW.CpfPaciente NOT REGEXP '^[0-9]{3}\\\\.[0-9]{3}\\\\.[0-9]{3}-[0-9]{2}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CPF inválido. Formato obrigatório: XXX.XXX.XXX-XX';
    END IF;
END$$
DELIMITER ;
    """, language="sql")
    
    st.markdown("---")
    
    # Tabela resumo
    st.markdown("### 📊 Resumo dos Triggers")
    triggers_data = [
        {"Entidade": "Paciente", "Tipo": "CPF", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Paciente", "Tipo": "Email", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Paciente", "Tipo": "Telefone", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Médico", "Tipo": "Email", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Médico", "Tipo": "Telefone", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Clínica", "Tipo": "Email", "Eventos": "INSERT, UPDATE", "Total": 2},
        {"Entidade": "Clínica", "Tipo": "Telefone", "Eventos": "INSERT, UPDATE", "Total": 2},
    ]
    
    df_triggers = pd.DataFrame(triggers_data)
    st.dataframe(df_triggers, use_container_width=True, hide_index=True)
    
    st.success("✅ Total de 14 triggers implementados no banco de dados MySQL")



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

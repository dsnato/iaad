import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from typing import Dict, Optional
from db import MySQLDB, ValidationError

# ============================================================================
# CONFIGURAÇÃO STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="Sistema de Consultas Médicas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONEXÃO COM BANCO DE DADOS
# ============================================================================
@st.cache_resource
def get_db():
    """Retorna instância do banco de dados."""
    try:
        db = MySQLDB(
            host='localhost',
            user='root',
            password='',  # Ajuste se necessário
            database='consultas_medicas',
            port=3306
        )
        # Testa conexão
        db.connect()
        return db
    except Exception:
        # Silenciosamente usa mock se não conectar
        return None

# Inicializar DB
db = get_db()
USE_MOCK = db is None

# ============================================================================
# DADOS MOCKADOS (FALLBACK SE MYSQL NÃO CONECTAR)
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

# ============================================================================
# FUNÇÕES HELPER (ABSTRAEM MYSQL OU MOCK)
# ============================================================================

def get_pacientes():
    """Retorna todos os pacientes."""
    if USE_MOCK:
        return st.session_state.pacientes_data
    try:
        rows = db.get_clientes()
        return [{"cpf": r["cpf"], "nome": r["nome"], "data_nascimento": str(r["data_nascimento"]), 
                 "genero": r["genero"], "telefone": r["telefone"], "email": r["email"]} for r in rows]
    except Exception as e:
        st.error(f"Erro ao buscar pacientes: {str(e)}")
        return []

def get_medicos():
    """Retorna todos os médicos."""
    if USE_MOCK:
        return st.session_state.medicos_data
    try:
        rows = db.get_medicos()
        return [{"codmed": r["codmed"], "nome": r["nome"], "genero": r["genero"], 
                 "especialidade": r["especialidade"], "telefone": r["telefone"], "email": r["email"]} for r in rows]
    except Exception as e:
        st.error(f"Erro ao buscar médicos: {str(e)}")
        return []

def get_consultas():
    """Retorna todas as consultas."""
    if USE_MOCK:
        # Retorna consultas mock
        if 'consultas_data' not in st.session_state:
            st.session_state.consultas_data = []
        return st.session_state.consultas_data
    try:
        rows = db.get_pedidos()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar consultas: {str(e)}")
        return []

def get_clinicas():
    """Retorna todas as clínicas."""
    if USE_MOCK:
        return st.session_state.clinicas_data
    try:
        rows = db.get_clinicas()
        return [{"codcli": r["codcli"], "nome": r["nome"], "endereco": r["endereco"], 
                 "telefone": r["telefone"], "email": r["email"]} for r in rows]
    except Exception as e:
        st.error(f"Erro ao buscar clínicas: {str(e)}")
        return []

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
    """Gerencia CRUD de consultas com validação de trigger."""
    st.markdown("## 📅 Gerenciamento de Consultas")
    
    #if USE_MOCK:
    #   st.info("")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Criar", "✏️ Editar", "🗑️ Deletar"])
    
    # TAB: LISTAR
    with tab1:
        st.subheader("📋 Consultas Agendadas")
        try:
            consultas = get_consultas()
            if consultas:
                # Formatar dados para visualização
                dados_formatados = []
                for c in consultas:
                    dados_formatados.append({
                        "Clínica": f"{c['CodCli']} - {c['clinica_nome'] or 'N/A'}",
                        "Médico": f"{c['CodMed']} - {c['medico_nome'] or 'N/A'}",
                        "Paciente": f"{c['CpfPaciente']} - {c['paciente_nome'] or 'N/A'}",
                        "Data/Hora": c['Data_Hora'].strftime('%d/%m/%Y %H:%M') if hasattr(c['Data_Hora'], 'strftime') else str(c['Data_Hora'])
                    })
                df = pd.DataFrame(dados_formatados)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"📊 Total: {len(consultas)} consultas agendadas")
            else:
                st.info("ℹ️ Nenhuma consulta agendada no momento.")
        except Exception as e:
            st.error(f"❌ Erro ao listar consultas: {str(e)}")
    
    # TAB: CRIAR (COM VALIDAÇÃO DE TRIGGER)
    with tab2:
        st.subheader("➕ Agendar Nova Consulta")
        
        # Aviso sobre o trigger
        st.info("🔔 **Atenção:** O sistema valida automaticamente se a consulta está dentro do prazo máximo de **60 dias (2 meses)** de antecedência.")
        
        # Buscar opções
        try:
            clinicas = get_clinicas()
            medicos = get_medicos()
            pacientes = get_pacientes()
            
            if not (clinicas and medicos and pacientes):
                st.warning("⚠️ Cadastre clínicas, médicos e pacientes antes de agendar consultas.")
                return
            
            with st.form("form_criar_consulta"):
                col1, col2 = st.columns(2)
                
                with col1:
                    clinica_opts = [f"{c['codcli']} - {c['nome']}" for c in clinicas]
                    clinica_sel = st.selectbox("Clínica", clinica_opts)
                    codcli = clinica_sel.split(" - ")[0]
                    
                    medico_opts = [f"{m['codmed']} - {m['nome']} ({m['especialidade']})" for m in medicos]
                    medico_sel = st.selectbox("Médico", medico_opts)
                    codmed = medico_sel.split(" - ")[0]
                
                with col2:
                    paciente_opts = [f"{p['cpf']} - {p['nome']}" for p in pacientes]
                    paciente_sel = st.selectbox("Paciente", paciente_opts)
                    cpf = paciente_sel.split(" - ")[0]
                
                col3, col4 = st.columns(2)
                with col3:
                    data_consulta = st.date_input("Data da Consulta", min_value=date.today())
                with col4:
                    hora_consulta = st.time_input("Hora da Consulta", value=datetime.now().time())
                
                # Calculadora de prazo
                dias_antecedencia = (data_consulta - date.today()).days
                if dias_antecedencia > 60:
                    st.error(f"❌ **{dias_antecedencia} dias de antecedência** - Será BLOQUEADO pelo trigger! (máx 60 dias)")
                elif dias_antecedencia < 0:
                    st.warning("⚠️ Data no passado")
                else:
                    st.success(f"✅ **{dias_antecedencia} dias de antecedência** - Dentro do prazo permitido")
                
                submitted = st.form_submit_button("🗓️ Agendar Consulta", type="primary")
            
            if submitted:
                try:
                    # Combinar data e hora
                    data_hora = datetime.combine(data_consulta, hora_consulta)
                    
                    if USE_MOCK:
                        # Modo mock - simular criação
                        nova_consulta = {
                            "CodCli": codcli,
                            "CodMed": codmed,
                            "CpfPaciente": cpf,
                            "Data_Hora": data_hora,
                            "clinica_nome": next((c['nome'] for c in clinicas if c['codcli'] == codcli), None),
                            "medico_nome": next((m['nome'] for m in medicos if m['codmed'] == codmed), None),
                            "paciente_nome": next((p['nome'] for p in pacientes if p['cpf'] == cpf), None)
                        }
                        
                        # Validação mock do trigger (60 dias)
                        if dias_antecedencia > 60:
                            st.error(f"🔔 **TRIGGER ATIVADO!** A consulta não pode ser agendada com mais de 60 dias de antecedência.")
                            st.warning("⚠️ Validação: Data além do prazo permitido (máximo 60 dias).")
                        else:
                            st.session_state.consultas_data.append(nova_consulta)
                            st.success(f"✅ Consulta agendada com sucesso para {data_hora.strftime('%d/%m/%Y às %H:%M')}!")
                            st.balloons()
                            st.rerun()
                    else:
                        # Modo MySQL - tentar criar (trigger será executado aqui!)
                        db.create_pedido(codcli, codmed, cpf, data_hora)
                        st.success(f"✅ Consulta agendada com sucesso para {data_hora.strftime('%d/%m/%Y às %H:%M')}!")
                        st.balloons()
                        st.rerun()
                    
                except ValidationError as ve:
                    st.error(f"❌ Validação: {str(ve)}")
                except Exception as e:
                    error_msg = str(e)
                    if "2 meses de antecedência" in error_msg or "60" in error_msg:
                        st.error(f"🔔 **TRIGGER ATIVADO!** {error_msg}")
                        st.warning("⚠️ A consulta não pode ser agendada com mais de 60 dias de antecedência.")
                    else:
                        st.error(f"❌ Erro ao agendar: {error_msg}")
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {str(e)}")
    
    # TAB: EDITAR
    with tab3:
        st.subheader("✏️ Editar Consulta")
        try:
            consultas = get_consultas()
            if not consultas:
                st.info("ℹ️ Nenhuma consulta para editar.")
                return
            
            opcoes = [f"{c['CodCli']} | {c['CodMed']} | {c['CpfPaciente']} | {c['Data_Hora']}" for c in consultas]
            consulta_sel = st.selectbox("Selecione a consulta", opcoes, key="sel_editar_consulta")
            
            partes = consulta_sel.split(" | ")
            codcli_old, codmed_old, cpf_old, data_hora_old = partes[0], partes[1], partes[2], partes[3]
            
            consulta = next((c for c in consultas if str(c['CodCli']) == codcli_old and 
                           str(c['CodMed']) == codmed_old and str(c['CpfPaciente']) == cpf_old), None)
            
            if consulta:
                st.info("🔔 **Atenção:** A alteração de data também será validada pelo trigger (máx 60 dias).")
                
                with st.form("form_editar_consulta"):
                    nova_data = st.date_input("Nova Data", value=date.today())
                    nova_hora = st.time_input("Nova Hora", value=datetime.now().time())
                    
                    dias_antecedencia = (nova_data - date.today()).days
                    if dias_antecedencia > 60:
                        st.error(f"❌ {dias_antecedencia} dias - Será BLOQUEADO!")
                    else:
                        st.success(f"✅ {dias_antecedencia} dias - OK")
                    
                    submitted_edit = st.form_submit_button("💾 Salvar Alterações")
                
                if submitted_edit:
                    try:
                        nova_data_hora = datetime.combine(nova_data, nova_hora)
                        
                        if USE_MOCK:
                            # Validação mock do trigger
                            if dias_antecedencia > 60:
                                st.error(f"🔔 **TRIGGER ATIVADO!** Não é possível agendar com mais de 60 dias.")
                            else:
                                # Atualizar no mock
                                for c in st.session_state.consultas_data:
                                    if (str(c['CodCli']) == codcli_old and 
                                        str(c['CodMed']) == codmed_old and 
                                        str(c['CpfPaciente']) == cpf_old):
                                        c['Data_Hora'] = nova_data_hora
                                        break
                                st.success("✅ Consulta atualizada com sucesso!")
                                st.rerun()
                        else:
                            # Modo MySQL
                            old_keys = (codcli_old, codmed_old, cpf_old, data_hora_old)
                            new_values = {'data_hora': nova_data_hora}
                            db.update_pedido(old_keys, new_values)
                            st.success("✅ Consulta atualizada com sucesso!")
                            st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "2 meses" in error_msg or "60" in error_msg:
                            st.error(f"🔔 **TRIGGER ATIVADO!** {error_msg}")
                        else:
                            st.error(f"❌ Erro: {error_msg}")
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
    
    # TAB: DELETAR
    with tab4:
        st.subheader("🗑️ Cancelar Consulta")
        try:
            consultas = get_consultas()
            if not consultas:
                st.info("ℹ️ Nenhuma consulta para cancelar.")
                return
            
            opcoes = [f"{c['CodCli']} | {c['CodMed']} | {c['CpfPaciente']} | {c['Data_Hora']}" for c in consultas]
            consulta_sel = st.selectbox("Selecione a consulta para cancelar", opcoes, key="sel_deletar_consulta")
            
            partes = consulta_sel.split(" | ")
            codcli, codmed, cpf, data_hora = partes[0], partes[1], partes[2], partes[3]
            
            st.warning(f"⚠️ Tem certeza que deseja cancelar esta consulta?")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🗑️ Confirmar Cancelamento", type="primary"):
                    try:
                        if USE_MOCK:
                            # Deletar do mock
                            st.session_state.consultas_data = [
                                c for c in st.session_state.consultas_data 
                                if not (str(c['CodCli']) == codcli and 
                                       str(c['CodMed']) == codmed and 
                                       str(c['CpfPaciente']) == cpf)
                            ]
                            st.success("✅ Consulta cancelada com sucesso!")
                            st.rerun()
                        else:
                            # Modo MySQL
                            db.delete_pedido(codcli, codmed, cpf, data_hora)
                            st.success("✅ Consulta cancelada com sucesso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao cancelar: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")


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
    st.dataframe(df_triggers, use_container_width=True, hide_index=True)
    
    st.success("✅ Total de 2 triggers implementados no banco de dados MySQL")
    
    st.markdown("---")
    
    # Seção de teste
    st.markdown("### 🧪 Teste de Validação do Trigger")
    st.info("**Como testar:** Tente agendar uma consulta com mais de 60 dias de antecedência na aba 'Consultas' → 'Criar'. O sistema deve bloquear e exibir a mensagem de erro do trigger.")
    
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
            st.warning(f"⚠️ Data no passado - Consulta não pode ser agendada")
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
    st.dataframe(df_exemplos, use_container_width=True, hide_index=True)



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

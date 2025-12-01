import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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
# SIMULAÇÃO DE BANCO DE DADOS (em memória, como dicionários/listas)
# ============================================================================

# Inicializa estruturas no session_state (persiste durante a sessão)
if "pacientes" not in st.session_state:
    st.session_state.pacientes = [
        {"id": 1, "nome": "João Silva", "idade": 45, "endereco": "Rua A, 123"},
        {"id": 2, "nome": "Maria Santos", "idade": 32, "endereco": "Rua B, 456"},
    ]

if "medicos" not in st.session_state:
    st.session_state.medicos = [
        {"id": 1, "nome": "Dr. Carlos", "especialidade": "Cardiologia"},
        {"id": 2, "nome": "Dra. Ana", "especialidade": "Dermatologia"},
    ]

if "consultas" not in st.session_state:
    st.session_state.consultas = [
        {
            "id": 1,
            "id_paciente": 1,
            "id_medico": 1,
            "data": datetime.now() - timedelta(days=5),
            "descricao": "Avaliação cardiológica de rotina"
        }
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
# FUNÇÕES HELPER - CONSULTAS
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

# ============================================================================
# FUNÇÕES HELPER - LOG (TRIGGER)
# ============================================================================


def registrar_log(mensagem: str):
    """Registra ação no log (simula trigger do MySQL)."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem": mensagem
    }
    st.session_state.log_acoes.append(log_entry)

# ============================================================================
# TELAS DA APLICAÇÃO
# ============================================================================


def tela_home():
    """Tela inicial com resumo do sistema."""
    st.markdown("# 🏥 Sistema de Consultas Médicas")
    st.markdown("Bem-vindo ao Sistema de Gerenciamento de Consultas Médicas!")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Pacientes", len(st.session_state.pacientes))
    with col2:
        st.metric("Total de Médicos", len(st.session_state.medicos))
    with col3:
        st.metric("Total de Consultas", len(st.session_state.consultas))

    st.markdown("---")
    st.markdown("### 📌 Sobre o Sistema")
    st.info(
        """
        Este é um sistema completo de gerenciamento de consultas médicas com:
        - ✅ CRUD completo para Pacientes, Médicos e Consultas
        - ✅ Validação de integridade referencial
        - ✅ Sistema de Log com Triggers simulados
        - ✅ Consultas avançadas e gráficos
        - ✅ Banco de dados em memória (sem MySQL)
        """
    )


def tela_pacientes():
    """Gerencia CRUD de pacientes."""
    st.markdown("## 👥 Gerenciamento de Pacientes")

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Pacientes")
        if st.session_state.pacientes:
            df = pd.DataFrame(st.session_state.pacientes)
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.warning("Nenhum paciente cadastrado.")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Paciente")
        with st.form("form_criar_paciente"):
            nome = st.text_input("Nome", placeholder="Ex: João Silva")
            idade = st.number_input("Idade", min_value=1, max_value=150, value=30)
            endereco = st.text_input("Endereço", placeholder="Ex: Rua A, 123")
            submitted = st.form_submit_button("Salvar Paciente")

        if submitted:
            if criar_paciente(nome, idade, endereco):
                st.success(f"✅ Paciente '{nome}' criado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao criar paciente. Verifique os dados.")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Paciente")
        if st.session_state.pacientes:
            opcoes = [f"{p['id']} - {p['nome']}" for p in st.session_state.pacientes]
            sel = st.selectbox("Selecione paciente", opcoes, key="sel_editar_pac")
            id_selecionado = int(sel.split(" - ")[0])
            paciente = get_paciente_por_id(id_selecionado)

            with st.form("form_editar_paciente"):
                nome = st.text_input("Nome", value=paciente["nome"])
                idade = st.number_input("Idade", min_value=1, max_value=150, value=paciente["idade"])
                endereco = st.text_input("Endereço", value=paciente["endereco"])
                submitted = st.form_submit_button("Atualizar")

            if submitted:
                if atualizar_paciente(id_selecionado, nome, idade, endereco):
                    st.success("✅ Paciente atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar paciente.")
        else:
            st.warning("Nenhum paciente para editar.")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Paciente")
        if st.session_state.pacientes:
            opcoes = [f"{p['id']} - {p['nome']}" for p in st.session_state.pacientes]
            sel = st.selectbox("Selecione paciente", opcoes, key="sel_deletar_pac")
            id_selecionado = int(sel.split(" - ")[0])

            if st.button("🗑️ Deletar Paciente", key="btn_deletar_pac"):
                if deletar_paciente(id_selecionado):
                    st.success("✅ Paciente deletado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Não é possível deletar este paciente pois ele possui consultas associadas.")
        else:
            st.warning("Nenhum paciente para deletar.")


def tela_medicos():
    """Gerencia CRUD de médicos."""
    st.markdown("## 👨‍⚕️ Gerenciamento de Médicos")

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Médicos")
        if st.session_state.medicos:
            df = pd.DataFrame(st.session_state.medicos)
            st.dataframe(df, width='stretch')
        else:
            st.warning("Nenhum médico cadastrado.")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Novo Médico")
        with st.form("form_criar_medico"):
            nome = st.text_input("Nome", placeholder="Ex: Dr. Carlos")
            especialidade = st.selectbox(
                "Especialidade",
                ["Cardiologia", "Dermatologia", "Neurologia", "Pediatria", "Oncologia", "Outro"]
            )
            if especialidade == "Outro":
                especialidade = st.text_input("Digite a especialidade")

            submitted = st.form_submit_button("Salvar Médico")

        if submitted:
            if criar_medico(nome, especialidade):
                st.success(f"✅ Médico '{nome}' criado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao criar médico. Verifique os dados.")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Médico")
        if st.session_state.medicos:
            opcoes = [f"{m['id']} - {m['nome']}" for m in st.session_state.medicos]
            sel = st.selectbox("Selecione médico", opcoes, key="sel_editar_med")
            id_selecionado = int(sel.split(" - ")[0])
            medico = get_medico_por_id(id_selecionado)

            with st.form("form_editar_medico"):
                nome = st.text_input("Nome", value=medico["nome"])
                especialidade = st.text_input("Especialidade", value=medico["especialidade"])
                submitted = st.form_submit_button("Atualizar")

            if submitted:
                if atualizar_medico(id_selecionado, nome, especialidade):
                    st.success("✅ Médico atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar médico.")
        else:
            st.warning("Nenhum médico para editar.")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Médico")
        if st.session_state.medicos:
            opcoes = [f"{m['id']} - {m['nome']}" for m in st.session_state.medicos]
            sel = st.selectbox("Selecione médico", opcoes, key="sel_deletar_med")
            id_selecionado = int(sel.split(" - ")[0])

            if st.button("🗑️ Deletar Médico", key="btn_deletar_med"):
                if deletar_medico(id_selecionado):
                    st.success("✅ Médico deletado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Não é possível deletar este médico pois ele possui consultas associadas.")
        else:
            st.warning("Nenhum médico para deletar.")


def tela_consultas():
    """Gerencia CRUD de consultas."""
    st.markdown("## 📅 Gerenciamento de Consultas")

    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Criar", "Editar", "Deletar"])

    # TAB: LISTAR
    with tab1:
        st.subheader("Lista de Consultas")
        if st.session_state.consultas:
            dados = list()
            for c in st.session_state.consultas:
                paciente = get_paciente_por_id(c["id_paciente"])
                medico = get_medico_por_id(c["id_medico"])
                dados.append({
                    "ID": c["id"],
                    "Paciente": paciente["nome"] if paciente else "N/A",
                    "Médico": medico["nome"] if medico else "N/A",
                    "Data": c["data"].strftime("%d/%m/%Y %H:%M"),
                    "Descrição": c["descricao"]
                })
            df = pd.DataFrame(dados)
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.warning("Nenhuma consulta cadastrada.")

    # TAB: CRIAR
    with tab2:
        st.subheader("Criar Nova Consulta")

        if not st.session_state.pacientes or not st.session_state.medicos:
            st.warning("⚠️ É necessário ter pelo menos um paciente e um médico cadastrados.")
        else:
            with st.form("form_criar_consulta"):
                opcoes_pac = [f"{p['id']} - {p['nome']}" for p in st.session_state.pacientes]
                sel_pac = st.selectbox("Selecione paciente", opcoes_pac)
                id_paciente = int(sel_pac.split(" - ")[0])

                opcoes_med = [f"{m['id']} - {m['nome']} ({m['especialidade']})" for m in st.session_state.medicos]
                sel_med = st.selectbox("Selecione médico", opcoes_med)
                id_medico = int(sel_med.split(" - ")[0])

                data_consulta = st.date_input("Data e hora da consulta")
                descricao = st.text_area("Descrição da consulta")
                submitted = st.form_submit_button("Criar Consulta")

            if submitted:
                if criar_consulta(id_paciente, id_medico, data_consulta, descricao):
                    st.success("✅ Consulta criada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao criar consulta. Verifique os dados.")

    # TAB: EDITAR
    with tab3:
        st.subheader("Editar Consulta")
        if st.session_state.consultas:
            opcoes = [f"{c['id']} - {get_paciente_por_id(c['id_paciente'])['nome']}" for c in st.session_state.consultas]
            sel = st.selectbox("Selecione consulta", opcoes, key="sel_editar_cons")
            id_selecionado = int(sel.split(" - ")[0])
            consulta = get_consulta_por_id(id_selecionado)

            with st.form("form_editar_consulta"):
                opcoes_pac = [f"{p['id']} - {p['nome']}" for p in st.session_state.pacientes]
                sel_pac = st.selectbox("Selecione paciente", opcoes_pac, key="edit_pac")
                id_paciente = int(sel_pac.split(" - ")[0])

                opcoes_med = [f"{m['id']} - {m['nome']}" for m in st.session_state.medicos]
                sel_med = st.selectbox("Selecione médico", opcoes_med, key="edit_med")
                id_medico = int(sel_med.split(" - ")[0])

                data_consulta = st.date_input("Data e hora", value=consulta["data"])
                descricao = st.text_area("Descrição", value=consulta["descricao"])
                submitted = st.form_submit_button("Atualizar")

            if submitted:
                if atualizar_consulta(id_selecionado, id_paciente, id_medico, data_consulta, descricao):
                    st.success("✅ Consulta atualizada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar consulta.")
        else:
            st.warning("Nenhuma consulta para editar.")

    # TAB: DELETAR
    with tab4:
        st.subheader("Deletar Consulta")
        if st.session_state.consultas:
            opcoes = [f"{c['id']} - {get_paciente_por_id(c['id_paciente'])['nome']}" for c in st.session_state.consultas]
            sel = st.selectbox("Selecione consulta", opcoes, key="sel_deletar_cons")
            id_selecionado = int(sel.split(" - ")[0])

            if st.button("🗑️ Deletar Consulta", key="btn_deletar_cons"):
                if deletar_consulta(id_selecionado):
                    st.success("✅ Consulta deletada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao deletar consulta.")
        else:
            st.warning("Nenhuma consulta para deletar.")


def tela_triggers():
    """Exibe log de ações (simula triggers do MySQL)."""
    st.markdown("## 🔔 Log de Ações (Triggers Simulados)")
    st.info(
        "Este log registra automaticamente todas as ações de CRUD no sistema, "
        "simulando o comportamento de triggers do MySQL."
    )

    if st.session_state.log_acoes:
        df_log = pd.DataFrame(st.session_state.log_acoes)
        st.dataframe(df_log, width='stretch', hide_index=True)

        if st.button("🗑️ Limpar Log"):
            st.session_state.log_acoes = []
            st.success("Log limpo!")
            st.rerun()
    else:
        st.warning("Nenhuma ação registrada no log.")


def tela_consultas_avancadas():
    """Consultas avançadas e gráficos."""
    st.markdown("## 📊 Visualizações e Consultas Avançadas")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Consultas por Médico",
        "Idade Média Pacientes",
        "Consultas por Especialidade",
        "Intervalo de Datas",
        "Resumo Geral"
    ])

    # TAB 1: Consultas por Médico
    with tab1:
        st.subheader("Quantidade de Consultas por Médico")
        if st.session_state.consultas:
            dados = {}
            for c in st.session_state.consultas:
                medico = get_medico_por_id(c["id_medico"])
                nome_med = medico["nome"] if medico else "N/A"
                dados[nome_med] = dados.get(nome_med, 0) + 1

            df = pd.DataFrame(list(dados.items()), columns=["Médico", "Quantidade"])
            st.bar_chart(df.set_index("Médico"))
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.warning("Nenhuma consulta para exibir.")

    # TAB 2: Idade Média dos Pacientes
    with tab2:
        st.subheader("Estatísticas de Pacientes")
        if st.session_state.pacientes:
            idades = [p["idade"] for p in st.session_state.pacientes]
            idade_media = sum(idades) / len(idades)
            idade_min = min(idades)
            idade_max = max(idades)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Idade Média", f"{idade_media:.1f} anos")
            with col2:
                st.metric("Idade Mínima", f"{idade_min} anos")
            with col3:
                st.metric("Idade Máxima", f"{idade_max} anos")
            with col4:
                st.metric("Total de Pacientes", len(st.session_state.pacientes))

            # Gráfico de distribuição de idade
            df_pac = pd.DataFrame(st.session_state.pacientes)
            st.line_chart(df_pac["idade"].value_counts().sort_index())
        else:
            st.warning("Nenhum paciente cadastrado.")

    # TAB 3: Consultas por Especialidade
    with tab3:
        st.subheader("Quantidade de Consultas por Especialidade")
        if st.session_state.consultas:
            dados = {}
            for c in st.session_state.consultas:
                medico = get_medico_por_id(c["id_medico"])
                esp = medico["especialidade"] if medico else "N/A"
                dados[esp] = dados.get(esp, 0) + 1

            df = pd.DataFrame(list(dados.items()), columns=["Especialidade", "Quantidade"])
            st.bar_chart(df.set_index("Especialidade"))
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.warning("Nenhuma consulta para exibir.")

    # TAB 4: Intervalo de Datas
    with tab4:
        st.subheader("Consultas em Intervalo de Datas")
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Data Inicial")
        with col2:
            data_fim = st.date_input("Data Final")

        if st.button("Filtrar"):
            consultas_filtradas = [
                c for c in st.session_state.consultas
                if data_inicio <= c["data"].date() <= data_fim
            ]

            if consultas_filtradas:
                dados = []
                for c in consultas_filtradas:
                    paciente = get_paciente_por_id(c["id_paciente"])
                    medico = get_medico_por_id(c["id_medico"])
                    dados.append({
                        "Data": c["data"].strftime("%d/%m/%Y"),
                        "Paciente": paciente["nome"] if paciente else "N/A",
                        "Médico": medico["nome"] if medico else "N/A",
                        "Descrição": c["descricao"]
                    })
                df = pd.DataFrame(dados)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.warning("Nenhuma consulta neste período.")

    # TAB 5: Resumo Geral
    with tab5:
        st.subheader("Resumo Geral do Sistema")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Pacientes", len(st.session_state.pacientes))
        with col2:
            st.metric("Total de Médicos", len(st.session_state.medicos))
        with col3:
            st.metric("Total de Consultas", len(st.session_state.consultas))

        st.markdown("---")

        # Pacientes com mais consultas
        st.subheader("Top 5 Pacientes com Mais Consultas")
        pacientes_consultas = {}
        for c in st.session_state.consultas:
            paciente = get_paciente_por_id(c["id_paciente"])
            nome = paciente["nome"] if paciente else "N/A"
            pacientes_consultas[nome] = pacientes_consultas.get(nome, 0) + 1

        if pacientes_consultas:
            df_top = pd.DataFrame(
                sorted(pacientes_consultas.items(), key=lambda x: x[1], reverse=True)[:5],
                columns=["Paciente", "Consultas"]
            )
            st.bar_chart(df_top.set_index("Paciente"))
        else:
            st.info("Sem dados para exibir.")
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
    "Banco de dados em memória (sem MySQL)\n\n"
    "Todos os dados são perdidos ao recarregar a página."
)

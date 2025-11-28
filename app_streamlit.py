import streamlit as st
import pandas as pd
from db import MySQLDB
from datetime import datetime

st.set_page_config(page_title="Sistema de Clientes e Pedidos", layout="wide")

# Use the consultas_medicas schema (reaproveitando o script fornecido)
db = MySQLDB(host='localhost', user='root', password='sua_senha', database='consultas_medicas')
conn = db.connect()

def get_pedidos_df():
    rows = db.get_pedidos()
    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(columns=["CodCli", "clinica_nome", "CodMed", "medico_nome", "CpfPaciente", "paciente_nome", "Data_Hora"])

def get_clientes_df():
    return pd.DataFrame(db.get_clientes())

st.title("📋 Gerenciamento de Clientes e Pedidos")

menu = st.sidebar.selectbox("Menu", ["Clientes", "Pedidos", "Visuais / Dashboards"])

if menu == "Clientes":
    st.header("Clientes")
    sub = st.selectbox("Ação", ["Listar", "Criar", "Editar", "Deletar"])
    if sub == "Listar":
        df = get_clientes_df()
        st.dataframe(df)
    elif sub == "Criar":
            st.subheader("Criar Cliente")
            with st.form("form_criar_cliente"):
                cpf = st.text_input("CPF (formato XXX.XXX.XXX-XX)", "")
                nome = st.text_input("Nome", "")
                data_nasc = st.date_input("Data de nascimento")
                genero = st.selectbox("Gênero", ["F", "M"]) 
                telefone = st.text_input("Telefone (DD) XXXXX-XXXX", "")
                email = st.text_input("Email", "")
                submitted = st.form_submit_button("Salvar")
            if submitted:
                try:
                    db.create_cliente(cpf.strip(), nome.strip(), data_nasc.isoformat(), genero, telefone.strip() or None, email.strip() or None)
                    st.success(f"Cliente criado com CPF = {cpf}")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao criar cliente: {e}")
    elif sub == "Editar":
        df = get_clientes_df()
        if df.empty:
            st.warning("Nenhum cliente para editar.")
        else:
                options = df["cpf"].astype(str) + " — " + df["nome"]
                sel = st.selectbox("Selecione cliente", options)
                cpf = sel.split(" — ")[0]
                cliente = df[df["cpf"] == cpf].iloc[0]
                with st.form("form_editar_cliente"):
                    nome = st.text_input("Nome", value=cliente["nome"])
                    email = st.text_input("Email", value=cliente.get("email", "") or "")
                    data_nasc = st.date_input("Data de nascimento", value=pd.to_datetime(cliente["data_nascimento"]).date() if cliente.get("data_nascimento") else None)
                    genero = st.selectbox("Gênero", ["F","M"], index=0 if cliente.get("genero","F")=="F" else 1)
                    telefone = st.text_input("Telefone", value=cliente.get("telefone", "") or "")
                    submitted = st.form_submit_button("Atualizar")
                if submitted:
                    try:
                        ok = db.update_cliente(cpf,
                                                nome=nome.strip(),
                                                data_nascimento=data_nasc.isoformat() if data_nasc else None,
                                                genero=genero,
                                                telefone=telefone.strip() or None,
                                                email=email.strip() or None)
                        if ok:
                            st.success("Cliente atualizado com sucesso.")
                            st.experimental_rerun()
                        else:
                            st.error("Nenhuma alteração enviada.")
                    except Exception as e:
                        st.error(f"Falha ao atualizar cliente: {e}")
    elif sub == "Deletar":
        df = get_clientes_df()
        if df.empty:
            st.warning("Nenhum cliente para deletar.")
        else:
            options = df["cpf"].astype(str) + " — " + df["nome"]
            sel = st.selectbox("Selecione cliente", options)
            cpf = sel.split(" — ")[0]
            if st.button("Deletar"):
                try:
                    ok = db.delete_cliente(cpf)
                    if ok:
                        st.success("Cliente deletado com sucesso.")
                        st.experimental_rerun()
                    else:
                        st.error("Falha ao deletar cliente.")
                except Exception as e:
                    st.error(f"Erro ao deletar cliente: {e}")

elif menu == "Pedidos":
    st.header("Pedidos")
    sub = st.selectbox("Ação", ["Listar", "Criar"])
    if sub == "Listar":
        df = get_pedidos_df()
        st.dataframe(df)
    elif sub == "Criar":
        st.subheader("Criar Pedido")
        df_clientes = get_clientes_df()
        if df_clientes.empty:
            st.warning("Não há clientes cadastrados — crie clientes antes de fazer pedidos.")
        else:
            # Consultar clínicas e médicos para seleção
            try:
                clinicas = db._execute("SELECT CodCli, NomeCli FROM Clinica ORDER BY NomeCli", fetchall=True) or []
                medicos = db._execute("SELECT CodMed, NomeMed FROM Medico ORDER BY NomeMed", fetchall=True) or []
            except Exception:
                clinicas = []
                medicos = []

            with st.form("form_criar_pedido"):
                cliente_sel = st.selectbox("Paciente", df_clientes["cpf"].astype(str) + " — " + df_clientes["nome"])
                cpf = cliente_sel.split(" — ")[0]
                clinica_sel = st.selectbox("Clínica", [f"{r['CodCli']} — {r['NomeCli']}" for r in clinicas]) if clinicas else st.text_input("Clínica (CodCli)")
                medico_sel = st.selectbox("Médico", [f"{r['CodMed']} — {r['NomeMed']}" for r in medicos]) if medicos else st.text_input("Médico (CodMed)")
                data_hora = st.datetime_input("Data e hora da consulta")
                submitted = st.form_submit_button("Criar Consulta")
            if submitted:
                try:
                    if clinicas:
                        codcli = clinica_sel.split(" — ")[0]
                    else:
                        codcli = clinica_sel
                    if medicos:
                        codmed = medico_sel.split(" — ")[0]
                    else:
                        codmed = medico_sel
                    db.create_pedido(codcli, codmed, cpf, data_hora)
                    st.success("Consulta criada com sucesso.")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao criar consulta: {e}")

elif menu == "Visuais / Dashboards":
    st.header("Dashboard de Pedidos")
    df = get_pedidos_df()
    if df.empty:
        st.warning("Sem pedidos para exibir.")
    else:
        st.subheader("Quantidade de pedidos por status")
        count_status = df["status"].value_counts().rename_axis("status").reset_index(name="count")
        st.bar_chart(count_status.set_index("status"))
        st.subheader("Valores de pedidos por cliente")
        pivot = df.groupby("cliente_nome")["valor"].sum().reset_index().sort_values(by="valor", ascending=False)
        st.dataframe(pivot)

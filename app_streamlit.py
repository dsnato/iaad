import streamlit as st
import pandas as pd
from db import MySQLDB
from datetime import datetime

st.set_page_config(page_title="Sistema de Clientes e Pedidos", layout="wide")

db = MySQLDB(host='localhost', user='root', password='sua_senha', database='projeto_iaad')
conn = db.connect()

def get_pedidos_df():
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.pedido_id, p.cliente_id, c.nome as cliente_nome, p.valor, p.status, p.criado_em
        FROM pedidos p
        LEFT JOIN clientes c ON p.cliente_id = c.cliente_id
        ORDER BY p.criado_em DESC
    """
    )
    rows = cur.fetchall()
    cur.close()
    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(columns=["pedido_id", "cliente_id", "cliente_nome", "valor", "status", "criado_em"])

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
            nome = st.text_input("Nome", "")
            email = st.text_input("Email", "")
            data_nasc = st.date_input("Data de nascimento")
            cidade = st.text_input("Cidade", "")
            submitted = st.form_submit_button("Salvar")
        if submitted:
            cliente_id = db.create_cliente(nome.strip(), email.strip() or None, data_nasc.isoformat(), cidade.strip())
            st.success(f"Cliente criado com ID = {cliente_id}")
    elif sub == "Editar":
        df = get_clientes_df()
        if df.empty:
            st.warning("Nenhum cliente para editar.")
        else:
            options = df["cliente_id"].astype(str) + " — " + df["nome"]
            sel = st.selectbox("Selecione cliente", options)
            cliente_id = int(sel.split(" — ")[0])
            cliente = df[df["cliente_id"] == cliente_id].iloc[0]
            with st.form("form_editar_cliente"):
                nome = st.text_input("Nome", value=cliente["nome"])
                email = st.text_input("Email", value=cliente.get("email", "") or "")
                data_nasc = st.date_input("Data de nascimento", value=pd.to_datetime(cliente["data_nascimento"]).date() if cliente.get("data_nascimento") else None)
                cidade = st.text_input("Cidade", value=cliente.get("cidade", "") or "")
                submitted = st.form_submit_button("Atualizar")
            if submitted:
                ok = db.update_cliente(cliente_id,
                                        nome=nome.strip(),
                                        email=email.strip() or None,
                                        data_nascimento=data_nasc.isoformat() if data_nasc else None,
                                        cidade=cidade.strip())
                if ok:
                    st.success("Cliente atualizado com sucesso.")
                else:
                    st.error("Falha ao atualizar cliente.")
    elif sub == "Deletar":
        df = get_clientes_df()
        if df.empty:
            st.warning("Nenhum cliente para deletar.")
        else:
            options = df["cliente_id"].astype(str) + " — " + df["nome"]
            sel = st.selectbox("Selecione cliente", options)
            cliente_id = int(sel.split(" — ")[0])
            if st.button("Deletar"):
                ok = db.delete_cliente(cliente_id)
                if ok:
                    st.success("Cliente deletado com sucesso.")
                else:
                    st.error("Falha ao deletar cliente.")

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
            with st.form("form_criar_pedido"):
                cliente_sel = st.selectbox("Cliente", df_clientes["cliente_id"].astype(str) + " — " + df_clientes["nome"])
                cliente_id = int(cliente_sel.split(" — ")[0])
                valor = st.number_input("Valor do pedido", min_value=0.0, format="%.2f")
                status = st.selectbox("Status", ["novo", "processando", "concluído", "cancelado"])
                submitted = st.form_submit_button("Criar Pedido")
            if submitted:
                cur = conn.cursor()
                sql = "INSERT INTO pedidos (cliente_id, valor, status) VALUES (%s, %s, %s)"
                cur.execute(sql, (cliente_id, valor, status))
                conn.commit()
                cur.close()
                st.success("Pedido criado com sucesso.")
                st.experimental_rerun()

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

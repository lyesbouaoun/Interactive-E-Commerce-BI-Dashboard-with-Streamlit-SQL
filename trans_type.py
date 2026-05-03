import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def transct():
    st.title("Transactions")
    conn = sqlite3.connect("olist.db")
    ville = pd.read_sql("""SELECT DISTINCT customer_city FROM customers""",conn)
    ville_list = ["All"] + ville["customer_city"].dropna().tolist()
    city = st.sidebar.selectbox(
        "🏙️ City",
        ville_list
    )

    where_clause = ""

    if city != "All":
        where_clause = f"WHERE c.customer_city = '{city}'"

    query = f"""SELECT 
        p.payment_type,
            COUNT(*) as nb_transactions
        FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        {where_clause}
        GROUP BY p.payment_type
        ORDER BY nb_transactions DESC
        """
    df=pd.read_sql(query,conn)
    st.subheader("💳 Répartition des transactions par type de paiement")
    st.write("result",df)
    st.bar_chart(df.set_index("payment_type"))

    payments = pd.read_sql("SELECT * FROM payments", conn)
    bins=[0,100,500,1000,2000,5000,10000]
    payments["df_payments"] = pd.cut(payments["payment_value"],bins,labels=["0-100", "100-500", "500-1000", "1000-2000", "2000-5000", "5000-10000"])
    df1 = payments.groupby("df_payments")["payment_type"].count().reset_index()
    st.subheader("📊 Nombre de transactions par tranche de montant")
    st.write("result",df1)

    df = pd.read_sql("""
    SELECT 
        payment_type,
        COUNT(*) as nb_transactions,
        AVG(payment_value) as avg_amount,
        SUM(payment_value) as total_amount
    FROM payments
    GROUP BY payment_type
    ORDER BY total_amount DESC
    """, conn)

    st.subheader("💰 Performance des paiements par type (volume, moyenne, total)")

    st.dataframe(df)

    querry2 = f"""
    SELECT 
        CASE 
            WHEN payment_value < 100 THEN '0-100'
            WHEN payment_value < 500 THEN '100-500'
            WHEN payment_value < 1000 THEN '500-1000'
            WHEN payment_value < 2000 THEN '1000-2000'
            WHEN payment_value < 5000 THEN '2000-5000'
            ELSE '+5000'
        END as tranche,
        payment_type , COUNT(*) as nb_transactions,
        AVG(payment_value) as avg_amount,
        SUM(payment_value) as total_amount
        FROM payments
        GROUP BY payment_type,tranche     
    """
    df = pd.read_sql(querry2, conn)

    st.subheader("📊 Analyse croisée : tranche de montant vs type de paiement")

    st.dataframe(df)
    mode =pd.read_sql("""SELECT DISTINCT payment_type FROM payments""",conn)
    mode_type=["ALL"] + mode["payment_type"].dropna().tolist()
    mode_de_payment=st.sidebar.selectbox(
        "mode de payment",
        mode_type
    )
    where = ""
    if mode_de_payment != "ALL":
        where = f"WHERE payment_type = '{mode_de_payment}'"

    querry3 = f""" SELECT 
             CASE 
                WHEN payment_value < 100 THEN '0-100'
                WHEN payment_value < 500 THEN '100-500'
                WHEN payment_value < 1000 THEN '500-1000'
                WHEN payment_value < 2000 THEN '1000-2000'
                WHEN payment_value < 5000 THEN '2000-5000'
                ELSE '+5000'
            END as tranche,
            payment_type , COUNT(*) as nb_transactions,
            SUM(payment_value) as total_amount
            FROM payments
            {where}
            GROUP BY tranche, payment_type """


    df2 = pd.read_sql(querry3, conn)

    pivot = df2.pivot(
        index="tranche",
        columns="payment_type",
        values="total_amount"
    ).fillna(0)

    st.subheader("📈 Tableau croisé des montants par tranche et type de paiement")
    st.dataframe(pivot)
    st.subheader("📊 Total des paiements par tranche de montant")
    st.bar_chart(df2.set_index("tranche")["total_amount"])





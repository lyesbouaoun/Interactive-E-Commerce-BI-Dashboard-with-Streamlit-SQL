import streamlit as st
import sqlite3
import pandas as pd


def vente_date_produit():

    st.title("📈 Vente de produits par mois")

    conn = sqlite3.connect("olist.db")

    # liste produits
    produid = pd.read_sql(
        "SELECT DISTINCT product_category_name FROM products",
        conn
    )

    liste_produid =produid["product_category_name"].dropna().tolist()

    produit_li = st.selectbox(
        "📦 Catégorie produit",
        liste_produid
    )

    # filtre SQL
    where = f"WHERE p.product_category_name = '{produit_li}'"

    # requête SQL
    query = f"""
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) as mois,
        p.product_category_name,

        COUNT(*) as nombre_de_vente,

        SUM(oi.price) as recette

    FROM orders o

    JOIN order_items oi 
        ON o.order_id = oi.order_id

    JOIN products p 
        ON p.product_id = oi.product_id

    {where}

    GROUP BY mois, p.product_category_name

    ORDER BY mois
    """

    df1 = pd.read_sql(query, conn)

    st.dataframe(df1)

    # pivot CORRECT
    st.subheader("tableau de vente par mois de chaque produit")
    pivot = df1.pivot(
        index="mois",
        columns="product_category_name",
        values="nombre_de_vente"
    ).fillna(0)

    st.line_chart(pivot)
    st.write(pivot.shape)

    pivot_recette = df1.pivot(
        index="mois",
        columns="product_category_name",
        values="recette"
    ).fillna(0)
    st.line_chart(pivot_recette)
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def dacshboard():
    st.title(" Dacshboard")
    conn = sqlite3.connect("olist.db")
    kpi = pd.read_sql_query("""select
         COUNT(*) as total,
        SUM(price) as totale_payer,
        AVG(price) as moy_payer
     FROM order_items
    """, conn)

    col1,col2,col3 = st.columns(3)
    col1.metric("totale transaction",int(kpi["totale_payer"][0]))
    col2.metric("moyenne_payer",round(kpi["moy_payer"][0]),2)
    col3.metric("totale_payer",round(kpi["totale_payer"][0]),2)

    # afficher totale pris par produit
    st.subheader("📦 Chiffre d’affaires par catégorie de produit")
    categorie = pd.read_sql_query("""
    select p.product_category_name , SUM(o.price) as totale_payer
    FROM order_items o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_category_name
    ORDER BY totale_payer DESC
    """,conn)

    st.bar_chart(categorie.set_index("product_category_name"))

    #afficher totale payer par chaque ville
    st.subheader("🏙️ Répartition des ventes par ville")
    ville = pd.read_sql_query("""
        SELECT c.customer_city , SUM(p.price) as totale_payer
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items p ON o.order_id= p.order_id
        GROUP BY c.customer_city
        """,conn)

    st.bar_chart(ville.set_index("customer_city"))

def filtre():
    conn = sqlite3.connect("olist.db")

    st.title("🎛️ Analyse dynamique des ventes")
    price_range = pd.read_sql("""
    SELECT MIN(price) as min_price, MAX(price) as max_price
    FROM order_items
    """, conn)

    min_db = float(price_range["min_price"][0])
    max_db = float(price_range["max_price"][0])

    min_val, max_val = st.sidebar.slider(
        "💰 Amount range",
        min_db,
        max_db,
        (min_db, max_db)
    )
    categories = pd.read_sql("""
    SELECT DISTINCT product_category_name 
    FROM products
    """, conn)

    # ajouter "All"
    category_list = ["All"] + categories["product_category_name"].dropna().tolist()

    category = st.sidebar.selectbox(
        "📦 Category",
        category_list
    )


    ville = pd.read_sql("""
    SELECT DISTINCT customer_city 
    FROM customers
    """, conn)
    villes_list=["All"] + ville["customer_city"].dropna().tolist()
    city = st.sidebar.selectbox(
        "🏙️ City",
        villes_list
    )

    where_clause = f"""
        WHERE oi.price BETWEEN {min_val} AND {max_val}
        """

    if category != "All":
        where_clause += f" AND p.product_category_name = '{category}'"


    query = f"""
    SELECT 
        
       c.customer_city,COUNT(*) as groupe_city
        
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON oi.product_id = p.product_id
    {where_clause}
    GROUP BY c.customer_city
    """

    where_clause1 = f"""
            WHERE oi.price BETWEEN {min_val} AND {max_val}
            """
    if city != "All":
        where_clause1 += f" AND c.customer_city = '{city}'"
    query1 = f"""
        SELECT 
            p.product_category_name,COUNT(*) as transact
            
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON oi.product_id = p.product_id
        {where_clause1}
        GROUP BY p.product_category_name
        """

    df = pd.read_sql(query, conn)
    df1 = pd.read_sql(query1, conn)
    st.subheader("📦 Transactions par catégorie de produit")
    st.bar_chart(df1.set_index("product_category_name"))

    st.write("📊 Results", df)
    st.subheader("🏙️ Distribution des transactions par ville")

    st.write("📊 Results1", df1)

    st.subheader("📦 Sales by Category")

    st.bar_chart(df.set_index("customer_city"))










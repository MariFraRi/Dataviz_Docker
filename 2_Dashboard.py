import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Configurar la página
st.set_page_config(
    page_title="Dashboard de Educación Básica", 
    layout="wide",
    page_icon="📊"
)

# Cargar la base de datos
@st.cache_data
def load_data():
    return pd.read_csv("educacion_basica.csv")

df = load_data()

# Título y descripción
st.title("📊 Dashboard de Educación Básica en Colombia")
st.markdown("""
Visualización interactiva de los datos de educación básica por departamento y categoría.
""")

# Dividir en columnas
col1, col2 = st.columns([1, 2])

with col1:
    # Filtros interactivos
    st.subheader("Filtros")
    departamentos = st.multiselect(
        "Seleccione departamentos",
        options=df['Departamento'].unique(),
        default=df['Departamento'].unique()[:3]
    )
    
    categorias = st.multiselect(
        "Seleccione categorías",
        options=df['Categoría'].unique(),
        default=df['Categoría'].unique()
    )
    
    rango_valores = st.slider(
        "Rango de valores",
        min_value=float(df['Valor'].min()),
        max_value=float(df['Valor'].max()),
        value=(float(df['Valor'].min()), float(df['Valor'].max()))
    )

# Aplicar filtros
df_filtrado = df[
    (df['Departamento'].isin(departamentos)) & 
    (df['Categoría'].isin(categorias)) &
    (df['Valor'].between(rango_valores[0], rango_valores[1]))
]

with col2:
    # Mostrar estadísticas básicas
    st.subheader("Resumen Estadístico")
    st.write(f"📌 Total de registros: {len(df_filtrado)}")
    st.write(f"📌 Valor promedio: {df_filtrado['Valor'].mean():.2f}")
    st.write(f"📌 Valor máximo: {df_filtrado['Valor'].max():.2f}")
    st.write(f"📌 Valor mínimo: {df_filtrado['Valor'].min():.2f}")

# Dividir en pestañas
tab1, tab2, tab3 = st.tabs(["📈 Gráficos", "🗃 Datos", "📊 Comparativas"])

with tab1:
    st.subheader("Distribución por Categoría")
    fig1 = px.histogram(
        df_filtrado, 
        x='Categoría',
        color='Categoría',
        title='Distribución de registros por categoría'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Valores por Departamento")
    fig2 = px.box(
        df_filtrado,
        x='Departamento',
        y='Valor',
        color='Categoría',
        title='Distribución de valores por departamento'
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Datos Filtrados")
    st.dataframe(df_filtrado.sort_values('Valor', ascending=False))
    
    # Opción para descargar datos filtrados
    st.download_button(
        label="Descargar datos filtrados como CSV",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name='educacion_basica_filtrado.csv',
        mime='text/csv'
    )

with tab3:
    st.subheader("Comparativa Departamental")
    
    # Seleccionar métrica para comparación
    metrica = st.radio(
        "Seleccione métrica para comparar:",
        options=['Promedio', 'Suma', 'Conteo'],
        horizontal=True
    )
    
    # Calcular según métrica seleccionada
    if metrica == 'Promedio':
        data = df_filtrado.groupby(['Departamento', 'Categoría'])['Valor'].mean().reset_index()
    elif metrica == 'Suma':
        data = df_filtrado.groupby(['Departamento', 'Categoría'])['Valor'].sum().reset_index()
    else:
        data = df_filtrado.groupby(['Departamento', 'Categoría']).size().reset_index(name='Conteo')
    
    # Gráfico de comparación
    fig4 = px.bar(
        data,
        x='Departamento',
        y='Valor' if metrica != 'Conteo' else 'Conteo',
        color='Categoría',
        barmode='group',
        title=f'Comparación por {metrica.lower()} entre departamentos'
    )
    st.plotly_chart(fig4, use_container_width=True)

# Notas al pie
st.markdown("---")
st.caption("Dashboard desarrollado con Streamlit - Datos de educación básica en Colombia")
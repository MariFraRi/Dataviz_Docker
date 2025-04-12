import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Configurar la página
st.set_page_config(page_title="Mapa Interactivo - Educación Básica", layout="wide")

st.title("📍 Mapa Interactivo de Educación Básica en Colombia")

# Cargar la base de datos con opción de upload
df = pd.read_csv("educacion_basica.csv")

# Convertir columnas a tipo numérico
df["Latitud"] = pd.to_numeric(df["Latitud"], errors="coerce")
df["Longitud"] = pd.to_numeric(df["Longitud"], errors="coerce")

# Eliminar filas con valores nulos en coordenadas
df = df.dropna(subset=["Latitud", "Longitud"])

# Sidebar para filtros
with st.sidebar:
    st.header("🔍 Filtros")
    
    # Filtrado por departamento
    departamentos = ["Todos"] + sorted(df["Departamento"].unique().tolist())
    departamento_seleccionado = st.selectbox("Departamento:", departamentos)
    
    # Filtrado por categoría
    categorias = ["Todas"] + sorted(df["Categoría"].unique().tolist())
    categoria_seleccionada = st.selectbox("Categoría:", categorias)
    
    # Filtrado por rango de valores
    if not df.empty:
        min_val, max_val = st.slider(
            "Rango de valores:",
            float(df["Valor"].min()),
            float(df["Valor"].max()),
            (float(df["Valor"].min()), float(df["Valor"].max()))
        )
    # Estadísticas
    st.header("📊 Estadísticas")
    if not df.empty:
        st.write(f"Total registros: {len(df)}")
        st.write(f"Valor promedio: {df['Valor'].mean():.2f}")
        st.write(f"Valor mínimo: {df['Valor'].min():.2f}")
        st.write(f"Valor máximo: {df['Valor'].max():.2f}")

# Aplicar filtros
if departamento_seleccionado != "Todos":
    df = df[df["Departamento"] == departamento_seleccionado]

if categoria_seleccionada != "Todas":
    df = df[df["Categoría"] == categoria_seleccionada]

if not df.empty:
    df = df[(df["Valor"] >= min_val) & (df["Valor"] <= max_val)]


# Crear el mapa base
m = folium.Map(location=[4.6097, -74.0818], zoom_start=6)


# Agregar cluster de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Definir colores por categoría
colores = {"Alta": "green", "Media": "orange", "Baja": "red"}

# Agregar marcadores al mapa
for _, row in df.iterrows():
    color = colores.get(row["Categoría"], "blue")
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=f"""
        <b>Departamento:</b> {row['Departamento']}<br>
        <b>Categoría:</b> {row['Categoría']}<br>
        <b>Valor:</b> {row['Valor']:.2f}<br>
        <b>Institución:</b> {row.get('Institución', 'N/A')}
        """,
        tooltip=row["Departamento"],
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(marker_cluster)

# Control de capas
folium.LayerControl().add_to(m)

# Mostrar el mapa
st.write("### Mapa de Educación Básica")
st.caption("Cada marcador representa una institución educativa. Puedes hacer zoom y click para más detalles.")
map_data = st_folium(m, width=1200, height=700)

# Mostrar datos filtrados
st.write("### Datos Filtrados")
st.dataframe(df)

# Botón para descargar datos filtrados
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos filtrados",
        data=csv,
        file_name='educacion_filtrada.csv',
        mime='text/csv'
    )

# Leyenda de colores
st.write("### Leyenda de Colores")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🟢 **Alta**: Buen desempeño")
with col2:
    st.markdown("🟠 **Media**: Desempeño intermedio")
with col3:
    st.markdown("🔴 **Baja**: Bajo desempeño")

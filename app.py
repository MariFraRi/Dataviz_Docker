import streamlit as st
from streamlit_option_menu import option_menu

# Configuración de página
st.set_page_config(
    page_title="Análisis Educativo Colombia", 
    layout="wide",
    page_icon="📚"
)

# Estilos CSS mejorados
st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    
    .section-title {
        color: #1a3e72;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 2px 5px;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

# Barra lateral de navegación
with st.sidebar:
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Inicio", "Visualización", "Dashboard"],
        icons=["house", "map", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "nav-link-selected": {"background-color": "gray"},
        }
    )

# Contenido de la página de Inicio
if selected == "Inicio":
    st.title("📊 Análisis de Educación Básica en Colombia")
    st.markdown("---")
    
    # Tarjeta de contextualización
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">CONTEXTUALIZACIÓN DE LOS DATOS</p>', unsafe_allow_html=True)
        st.markdown("""
        Los datos presentados corresponden a un conjunto de observaciones por departamento en Colombia. 
        Cada fila representa un departamento (o distrito capital, como <span style="background-color: white; color: black;">Bogotá D.C.</span>) 
        con información geográfica y categórica asociada a un valor numérico.
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### Estructura del Dataset:
        
        - **ID**: Identificador único de cada registro.
        - **Departamento**: Nombre del departamento colombiano.
        - **Latitud y Longitud**: Coordenadas geográficas del centro aproximado del departamento.
        - **Categoría**: Clasificación cualitativa (<span style="background-color: white; color: black;">A, B o C</span>) asignada a cada departamento.
        - **Valor**: Indicador cuantitativo normalizado (entre 0 y 1) que podría representar:
          - Métricas de desempeño educativo
          - Índices de desarrollo
          - Niveles de cumplimiento
          - Eficiencia en la gestión
        """, unsafe_allow_html=True)
        
        
    

elif selected == "Visualización":
    st.switch_page("pages/1_grafico.py")
    
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

ruta = 'https://github.com/FranckPy/ProyectoData/raw/refs/heads/main/df_limpio.csv'
df = pd.read_csv(ruta)

filas = df.shape[0] #Totalfamilias
variables = df.shape[1]
num_deptos = df['NombreDepartamentoAtencion'].nunique() #TotalDepartamentos
num_mpios = df['NombreMunicipioAtencion'].nunique() #TotalMunicipios
uni_deptos = df['NombreDepartamentoAtencion'].unique()
df_pivote = df.pivot_table(
    index = 'NombreDepartamentoAtencion',
    columns = 'Genero',
    values = ['CantidadDeBeneficiarios'],
    aggfunc = 'sum')
df_1 = df.groupby(['NombreDepartamentoAtencion', 'Genero'])['CantidadDeBeneficiarios'].sum().reset_index()
totBen = df['CantidadDeBeneficiarios'].sum() #Total Beneficiarios

# Promedio de beneficiarios por familia
promedio_beneficiarios_por_familia = df['CantidadBeneficioConsolidado'].mean()
# Promedio de beneficiarios por departamento
promedio_beneficiarios_por_departamento = df.groupby('NombreDepartamentoAtencion')['CantidadBeneficioConsolidado'].mean()
# Promedio de beneficiarios por municipio
promedio_beneficiarios_por_municipio = df.groupby('NombreMunicipioAtencion')['CantidadBeneficioConsolidado'].mean()

###############################################################################
#                            VISUALIZACIÓN EN STREAMLIT                       #
###############################################################################
st.set_page_config(
    page_title='BENEFICIARIOS DEL PROGRAMA FAMILIAS EN SU TIERRA',
    layout='centered')
st.markdown(
    '''
    <style>
        .block-container {
        max-width: 1200px;
        }

    ''',
    unsafe_allow_html=True
)

st.image('img/head.png')
st.caption('''Aplicación desarrollada por:
                                           Franck Henao Calderon - Franckh111@hotmail.com\\
                                           Luis Felipe Sánchez Gutierrez - Lfsg0695@gmail.com\\
                                           Brandon Rendon Herrera - Brandon.rendonno11@gmail.com\\
                                           Deisy González Sánchez - Daisyanahoj11@gmail.com\\
                                           Natalia Edith Piedrahita - nepmovistar@gmail.com''')
           
st.header('Análisis de datos')
st.subheader('Bootcamp Talento Tech')
st.title("Inicio")
# Texto introductorio
st.markdown("""
Bienvenido al panel de análisis de datos del programa **Familias en su Tierra**.
Aquí podrás explorar información sobre beneficiarios, características demográficas,
niveles de atención y otros indicadores clave mediante visualizaciones interactivas.
            
**Acerca del programa:** El programa Familias en su Tierra (FEST), liderado por Prosperidad Social, 
está orientado a promover la estabilización socioeconómica de hogares víctimas del desplazamiento, 
mediante procesos de acompañamiento familiar, fortalecimiento comunitario y apoyo a proyectos productivos. 
Como parte de un enfoque de inclusión social y productiva, FEST opera en diversos municipios priorizados del país, 
promoviendo la transformación de condiciones de vulnerabilidad.
""")

st.title("Análisis")
###############################################################################
#                        TAMAÑO DEL CONJUNTO DE DATOS                         #
###############################################################################


st.markdown('<a id="acerca-de"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Acerca del Conjunto de Datos</h2>')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Número de Variables', variables, border=True)

    with col2:
        st.metric('Número de Observaciones', filas, border=True)

    with col3:
        st.metric('Número de Departamentos', num_deptos, border=True)

    with col4:
        st.metric('Número de Municipios', num_mpios, border=True)

    if st.checkbox('Mostrar detalles el Dataset'):
        st.write('Conjuto de datos obtenidos del portal Datos.gov.co')
        st.write('Disponible en https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Beneficiarios-Familias-en-su-tierra/mebh-t5gy/about_data')

    with st.expander('Ver conjunto de datos completo'):
        st.dataframe(df)

    with st.expander('Ver Datos de Beneficiarios por Departamento y Género'):
        st.dataframe(df_pivote)

###############################################################################
#      GRAFICO INTERACTIVO DE BARRAS HORIZONTALES POR DEPARTAMENTO Y GENERO    #
###############################################################################
st.markdown('<a id="evolucion"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Beneficiarios por Departamento y Género</font>')

    # Desplegable para seleccionar departamento
    depto_selec = st.selectbox(
        'Selecciona un Departamento:',
        options=uni_deptos
    )
    condicion_filtro = df_1['NombreDepartamentoAtencion'] == depto_selec
    df_departamento = df_1[condicion_filtro]

    # Crear gráfico de barras horizontales
    # 1 Crear el objeto Figure
    fig_barras = go.Figure()

    # 2 Agregar las barras a fig_barras que es el objeto Figure
    fig_barras.add_trace(go.Bar(
        x=df_departamento['CantidadDeBeneficiarios'],
        y=df_departamento['Genero'].astype(str),
        orientation='h',
        marker_color='#9cca25',
        text=df_departamento['CantidadDeBeneficiarios'],
        texttemplate='%{text:,.0f}',
        textposition='auto',
    ))

    # 3. Actualizar el objeto Figure con el diseño deseado
    fig_barras.update_layout(
        height=400,
        xaxis_title='Cantidad de Beneficiarios',
        yaxis_title='Genero',
        showlegend=False,
        yaxis={'categoryorder': 'category ascending'}
    )

    # Mostrar
    st.plotly_chart(fig_barras, use_container_width=True)

###############################################################################
#           INDICADORES DE ENERGÍA ACTIVA POR AÑO EN MILLONES DE KWH          #
###############################################################################
st.title("Indicadores")
st.markdown('<a id="indicadores"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#55883B> Participación de Beneficiarios por Género</font>')

    # --- Cálculos ---
total = df["CantidadDeBeneficiarios"].sum()

# Variables con suma por género
hombres = df[df["Genero"] == "Hombre"]["CantidadDeBeneficiarios"].sum()
mujeres = df[df["Genero"] == "Mujer"]["CantidadDeBeneficiarios"].sum()
nd = df[df["Genero"] == "ND"]["CantidadDeBeneficiarios"].sum()
intersexual = df[df["Genero"] == "Intersexua"]["CantidadDeBeneficiarios"].sum()

# Mostrar en columnas de Streamlit
col5, col6, col7, col8 = st.columns(4)

col5.metric(label="Hombres", value=f"{hombres:,}")
col5.metric(label="% Hombres", value=f"{hombres / total * 100:.1f}%")

col6.metric(label="Mujeres", value=f"{mujeres:,}")
col6.metric(label="% Mujeres", value=f"{mujeres / total * 100:.1f}%")

col7.metric(label="Intersexual", value=f"{intersexual:,}")
col7.metric(label="% Intersexual", value=f"{intersexual / total * 100:.1f}%")

col8.metric(label="No Definido (ND)", value=f"{nd:,}")
col8.metric(label="% ND", value=f"{nd / total * 100:.1f}%")

st.write("CANTIDAD DE BENEFICIARIOS:", df["CantidadDeBeneficiarios"].sum())

###############################################################################
#    GRAFICO BARRAS DE ENERGÍA ACTIVA Y REACTIVA POR AÑO EN MILLONES DE KWH   #
###############################################################################
#Brandon

###############################################################################
#    GRAFICO TORTAS DE ENERGÍA ACTIVA Y REACTIVA POR AÑO EN MILLONES DE KWH   #
###############################################################################
#Brandon

###############################################################################
#                             MENU EN BARRA LATERAL                           #
###############################################################################
import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="PROYECTO FAMILIA EN SU TIERRA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Menú lateral ---
with st.sidebar:

    # Imagen en la parte superior del menú lateral
    st.image("img/FEST.png", width=160)
    
    # Título o encabezado del menú
    st.markdown("## Menú Principal")

    # Vínculos externos con markdown
    st.markdown("""
    ---
    ### Recursos útiles
    - [Datos abiertos](https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Beneficiarios-Familias-en-su-tierra/mebh-t5gy/about_data)
    - [Familias en su Tierra](https://prosperidadsocial.gov.co/sgpp/inclusion-productiva/familias-en-su-tierra/)
    - [GitHub del proyecto](https://github.com/FranckPy/ProyectoData)           ---
    """)

    # Radio para navegación interna (cambia contenido de la página principal)
    menu_opciones = st.radio(
        "Navega por secciones:", 
        ('Inicio', 'Análisis', 'Indicadores', 'Acerca de')
    )

    # Información clave o instrucciones en el menú lateral
    st.markdown("""
    ---
    **Información clave:**

    - Usa el menú para explorar.
    - Los datos se actualizan en tiempo real.
    -     ---
    """)

# --- Contenido principal ---
if menu_opciones == 'Inicio':
    st.title("Bienvenido a la app")
    st.write("Esta es la página principal donde puedes ver la descripción general.")
elif menu_opciones == 'Análisis':
    st.title("Análisis de Datos")
    st.write("Aquí puedes visualizar gráficos, tablas y análisis interactivos.")
elif menu_opciones == 'Indicadores':
    st.title("Indicadores Clave")
    st.write("Se presentan los indicadores y métricas importantes.")
elif menu_opciones == 'Acerca de':
    st.title("Acerca de este proyecto")
    st.write("""
    Esta app fue desarrollada como Proyecto Final del Programa de Talento Tech - Región 2.
    """)

# Pie de página o créditos
st.markdown("---")
st.caption("Desarrollado en Talento Tech/Análisis de Datos - 2025")

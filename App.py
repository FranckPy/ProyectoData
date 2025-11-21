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

#Dataframe agrupados para graficos Nivel escolaridad y Discapacidad
df_agrupado = (
    df.groupby(['Discapacidad', 'TipoBeneficio'])
      .size()
      .reset_index(name='conteo_Discapacidad')
)

df_agrupado_escolaridad = (
    df.groupby(['NivelEscolaridad', 'TipoBeneficio'])
      .size()
      .reset_index(name='conteo_NivelEscolaridad')
)

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
st.markdown('<a id="inicio"></a><br><br>', unsafe_allow_html=True)
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
st.markdown('<a id="objetivo"></a><br><br>', unsafe_allow_html=True)
st.title("Objetivo")
st.write("""
Realizar un análisis integral de la base de datos pública “*Beneficiarios Familias en su Tierra*”, 
con el fin de caracterizar la población beneficiaria, identificar patrones socioeconómicos, geográficos y demográficos, 
y evaluar elementos clave del impacto del programa en el contexto de inclusión social y transformación productiva, 
aplicando técnicas de análisis de datos vistas en el curso.
""")
st.markdown('<a id="analisis"></a><br><br>', unsafe_allow_html=True)
st.title("Análisis")
###############################################################################
#                        TAMAÑO DEL CONJUNTO DE DATOS                         #
###############################################################################
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
#           INDICADORES DE GENERO PRESENTES EN EL PROYECTO         #
###############################################################################
st.title("Indicadores")
st.markdown('<a id="indicadores"></a><br><br>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(
        """
        <div style='border: 3px solid #55883B; padding: 8px 12px; border-radius: 6px;'>
            <h3 style='color:#55883B;'>Participación de Beneficiarios por Género</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

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
#    GRAFICO DE BARRAS SOBRE CANTIDAD DE BENEFICIARIOS POR DISCAPACIDAD  #
###############################################################################
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Beneficios por estado de discapacidad</font>')

    col5 = st.columns(1)[0]

    with col5:
        # Ordenar y tomar Top 10
        df_mayores = df_agrupado.sort_values(
            by='conteo_Discapacidad',
            ascending=False
        ).head(10)

        # Crear figura horizontal con Plotly
        fig = px.bar(
            df_mayores,
            y='TipoBeneficio',
            x='conteo_Discapacidad',
            color='Discapacidad',
            orientation='h',
            
            labels={
                'Discapacidad': 'Estado de discapacidad',
                'conteo_Discapacidad': 'Cantidad de beneficiarios',
                'TipoBeneficio': 'Tipo de beneficio'
            },
            height=500,
            color_discrete_sequence=['#C1E899', '#9A6735', '#55883B','#E6F0DC', "#9cca25"]
        )

        # Ajustes visuales
        fig.update_traces(
            textposition='outside',
            texttemplate='%{x:,.0f}',
            hovertemplate=(
                "<b>Tipo de beneficio:</b> %{y}<br>"
                "<b>Cantidad beneficiarios:</b> %{x:,}<br>"
            )
        )

        fig.update_layout(
            showlegend=True,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#E5E5E5"),
            yaxis=dict(title='Tipo de Beneficio')
        )

        # Render en Streamlit
        st.plotly_chart(fig, width='stretch')

###############################################################################
#    BENEFICIOS OTORGADOS POR NIVEL DE ESCOLARIDAD   #
###############################################################################
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Beneficios por nivel de escolaridad</font>')

    col6 = st.columns(1)[0]

with col6:
        df_mayores = df_agrupado_escolaridad.sort_values(
            by='conteo_NivelEscolaridad',
            ascending=False
        ).head(25)

        fig = px.bar(
            df_mayores,
            y='TipoBeneficio',
            x='conteo_NivelEscolaridad',
            color='NivelEscolaridad',
            orientation='h',
            labels={
                'NivelEscolaridad': 'Nivel de escolaridad',
                'conteo_NivelEscolaridad': 'Cantidad de beneficiarios',
                'TipoBeneficio': 'Tipo de beneficio'
            },
            height=600,
            color_discrete_sequence=['#C1E899', '#9A6735', '#55883B','#E6F0DC', '#9cca25','#43ec7b']
        )

        fig.update_traces(
            textposition='outside',
            texttemplate='%{x:,.0f}',
            hovertemplate=(
                "<b>Tipo de beneficio:</b> %{y}<br>"
                "<b>Cantidad beneficiarios:</b> %{x:,}<br>"
            )
        )

        fig.update_layout(
            showlegend=True,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#E5E5E5"),
            yaxis=dict(title='Tipo de Beneficio')
        )

        st.plotly_chart(fig, width='stretch')

#################################################################
#    GRAFICO RELACION RANGO DE EDAD CON ESTADO BENEFICIARIO     #
#################################################################
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Heatmap Rango Edad vs Estado Beneficiario</font>')

    col9 = st.columns(1)[0]

    with col9:

        # Asegurar que RangoEdad es categoría
        df['RangoEdad'] = df['RangoEdad'].astype('category')

        # Tabla cruzada
        tabla = pd.crosstab(df['RangoEdad'], df['EstadoBeneficiario'])

        # Normalización
        tabla_norm = tabla.div(tabla.sum(axis=0), axis=1)

        # Transformar a listas ordenadas
        x_labels = tabla_norm.columns.tolist()
        y_labels = tabla_norm.index.tolist()

        fig = go.Figure(data=go.Heatmap(
            z=tabla_norm.values,
            x=x_labels,
            y=y_labels,
            colorscale=[
                [0.0, '#C1E899'],
                [0.25, '#9A6735'],
                [0.5, '#E6F0DC'],
                [0.75, '#55883B'],
                [1.0, '#D62728']
            ],
            zmin=0,
            zmax=1,
            colorbar=dict(title="Proporción")
        ))

        fig.update_traces(
            hovertemplate=
            "<b>RangoEdad:</b> %{y}<br>" +
            "<b>EstadoBeneficiario:</b> %{x}<br>" +
            "<b>Relación:</b> %{z:.2f}<extra></extra>"
        )

        fig.update_layout(
            width=900,
            height=600,
            xaxis_title="Estado Beneficiario",
            yaxis_title="Rango de Edad",
            xaxis=dict(tickangle=45),
            yaxis=dict(type='category')
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption("Mueva el cursor sobre las celdas para ver la proporción exacta (Tooltip).")

###############################################################################
#                             MENU EN BARRA LATERAL                           #
###############################################################################
# import streamlit as st

# # Configuración básica de la página
# st.set_page_config(
#     page_title="PROYECTO FAMILIA EN SU TIERRA",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

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
    - [GitHub del proyecto](https://github.com/FranckPy/ProyectoData)          
    ---
    """)

    # Secciones para navegación interna
    with st.sidebar.container():
        st.header("Navega por secciones:")
        st.markdown('[Inicio](#inicio)')
        st.markdown('[Objetivo](#objetivo)')
        st.markdown('[Análisis](#analisis)')
        st.markdown('[Indicadores](#indicadores')
        st.markdown('[Acerca de](#acerca-de)')

    # Información clave o instrucciones en el menú lateral
    st.markdown("""
    ---
    **Información clave:**

    - Usa el menú para explorar.
    - Los datos se actualizan en tiempo real.
    ---
    """)
st.markdown('<a id="acerca-de"></a><br><br>', unsafe_allow_html=True)
st.title("Acerca de este proyecto")
st.write("""
Este proyecto es el resultado del trabajo colaborativo desarrollado durante el curso de Análisis de Datos – Nivel Exploratorio, 
en el marco del Bootcamp de Talento Tech de la Universidad de Antioquia y el Ministerio de la TIC. Cada integrante aplicó los conocimientos adquiridos para transformar datos en 
insumos estratégicos, desde una perspectiva analítica, ética y orientada a la toma de decisiones.

Más que una aplicación, este trabajo refleja el compromiso, la evolución y la capacidad de adaptación de cada miembro del equipo frente 
a los retos del análisis de la información.

**Porque cuando el dato se interpreta con sentido, la tecnología deja de ser una herramienta y se convierte en oportunidad.**
""")

# Pie de página o créditos
st.markdown("---")
st.caption("Desarrollado en Talento Tech/Análisis de Datos - 2025")

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
                                           Luis Felipe Sanchez Gutierrez - Lfsg0695@gmail.com\\
                                           Brandon Rendon Herrera - Brandon.rendonno11@gmail.com\\
                                           Deisy Gonzalez - Daisyanahoj11@gmail.com\\
                                           Natalia Edith Piedrahita - nepmovistar@gmail.com''')
           
st.header('Análisis de datos')
st.subheader('Bootcamp Talento Tech')
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
        st.write('Conjuto de datos obtendios del portal Datos.gov.co')
        st.write('Disponible en https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Beneficiarios-Familias-en-su-tierra/mebh-t5gy/about_data')

    with st.expander('Ver conjunto de datos completo'):
        st.dataframe(df)

    with st.expander('Ver Datos de Beneficiarios por Departamento y Genero'):
        st.dataframe(df_pivote)

###############################################################################
#      GRAFICO INTERACTIVO DE BARRAS HORIZONTALES POR DEPARTAMENTO Y GENERO    #
###############################################################################
st.markdown('<a id="evolucion"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#55883B>Beneficiarios por Departamento y Genero</font>')

    # Desplegable para seleccionar departamento
    depto_selec = st.selectbox(
        'Selecciona un departamento:',
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
#Deisy

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
#Deisy
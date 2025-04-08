import streamlit as st
import pandas as pd
import numpy as np
from users import login, get_accessible_departments, get_accessible_employees, can_edit, USERS

st.set_page_config(page_title="Sistema de Evaluación de KPIs", layout="wide")

# Definición de departamentos y empleados
DEPARTAMENTOS = {
    "Diseño": ["Eduardo Alfaro", "Becario"],
    "Programación": ["Oscar Ramirez", "Ivan N.", "Nuevo"],
    "Hardware": ["Boris Gonzalez"],
    "Plataforma": ["Brenda Muñiz", "Jesus Dominguez", "Susana Hernandez", "Karla Luna", "Marco N."],
    "Coordinación Laboratorio": ["Alejandro Muñiz", "Otros"]
}

# Guardar departamentos en session_state para acceso desde users.py
st.session_state.departamentos = DEPARTAMENTOS

# KPIs por departamento/persona
KPIS = {
    "Eduardo Alfaro": {
        'KPI': [
            'Entregas a tiempo',
            '% de diseños aprobados en primer intento',
            'N° de materiales diseñados al mes',
            'Tasa de interacción con contenidos visuales',
            'Cumplimiento del manual de marca',
            'Satisfacción de equipos internos',
            'Errores post-publicación',
            'Cantidad de contenidos visuales publicados',
            'Impacto del contenido visual en redes',
            'Índice de innovación visual',
            'Colaboración efectiva con equipos',
            'Tiempo promedio de respuesta a solicitudes'
        ],
        'Descripción': [
            'Fechas de entrega planificadas vs reales; se califica el cumplimiento de los plazos.',
            'Número de diseños aceptados sin corrección; se califica la precisión y alineación con el briefing.',
            'Volumen de trabajo entregado; se califica la productividad mensual.',
            'Número de likes, comentarios y compartidos en relación a las impresiones; se califica la efectividad del diseño en redes.',
            'Revisión de cumplimiento con los lineamientos del manual de marca; se califica consistencia visual.',
            'Promedio de satisfacción de equipos internos en cuanto a calidad y tiempos; se califica percepción interna.',
            'Cantidad y tipo de errores visuales detectados tras publicación; se califica nivel de revisión previa.',
            'Cantidad de contenidos que efectivamente fueron publicados; se califica impacto y efectividad del trabajo entregado.',
            'Comparación del CTR visual o alcance con el promedio; se califica relevancia del contenido.',
            'Cantidad de piezas innovadoras (nuevos estilos, formatos); se califica creatividad e innovación.',
            'Resultados de encuestas sobre colaboración y comunicación; se califica el trabajo en equipo.',
            'Horas promedio desde solicitud hasta respuesta inicial; se califica nivel de respuesta y atención.'
        ],
        'Total': [1, 10, 10, 50, 10, 10, 10, 10, 100, 5, 5, 4],
        'Cumplimiento': [1, 10, 10, 10, 8, 10, 5, 10, 100, 5, 5, 5],
        'Ponderación': [10, 10, 8, 8, 8, 10, 8, 8, 8, 7, 7, 8]
    },
    "Oscar Ramirez": {
        'KPI': [
            'Entregas de código a tiempo',
            'Calidad del código',
            'Bugs resueltos',
            'Documentación del código',
            'Colaboración en equipo'
        ],
        'Descripción': [
            'Cumplimiento de fechas de entrega acordadas para desarrollo.',
            'Evaluación de la calidad y limpieza del código entregado.',
            'Cantidad de bugs resueltos vs reportados.',
            'Calidad y completitud de la documentación del código.',
            'Nivel de colaboración y comunicación con el equipo.'
        ],
        'Total': [10, 10, 20, 10, 5],
        'Cumplimiento': [0, 0, 0, 0, 0],
        'Ponderación': [25, 25, 20, 15, 15]
    }
}

# Función para obtener KPIs por defecto
def get_default_kpis():
    return {
        'KPI': ['Definiendo KPIs...'],
        'Descripción': ['KPIs en proceso de definición'],
        'Total': [0],
        'Cumplimiento': [0],
        'Ponderación': [100],
        'Resultado fórmula': [0],
        'Calificación': [0]
    }

# Función para mostrar la página de login
def show_login():
    st.title("Sistema de Evaluación de KPIs")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# Función para mostrar la página principal
def show_main():
    st.title("Sistema de Evaluación de KPIs")
    
    # Mostrar información del usuario
    st.sidebar.markdown(f"""
    ### Usuario: {USERS[st.session_state.user]['name']}
    **Rol**: {USERS[st.session_state.user]['role'].title()}
    """)
    
    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Obtener departamentos accesibles
    departamentos_accesibles = get_accessible_departments(st.session_state.user)
    
    # Selección de departamento y empleado
    col1, col2, col3 = st.columns(3)
    with col1:
        departamento = st.selectbox(
            "Seleccione Departamento",
            options=departamentos_accesibles,
            key="departamento"
        )

    with col2:
        empleados_accesibles = get_accessible_employees(st.session_state.user, departamento)
        empleado = st.selectbox(
            "Seleccione Empleado",
            options=empleados_accesibles,
            key="empleado"
        )

    with col3:
        st.date_input("Mes de evaluación", key="fecha_evaluacion")

    st.markdown("---")

    # Obtener KPIs según el empleado seleccionado
    if empleado in KPIS:
        initial_data = KPIS[empleado]
    else:
        initial_data = get_default_kpis()

    # Crear datos iniciales si no existen en la sesión o si cambia el empleado
    if 'data' not in st.session_state or 'current_employee' not in st.session_state or st.session_state.current_employee != empleado:
        st.session_state.data = pd.DataFrame(initial_data)
        st.session_state.current_employee = empleado
        st.session_state.resultado_final = 0

    # Editor de datos
    edited_df = st.data_editor(
        st.session_state.data,
        key="editor",
        disabled=not can_edit(st.session_state.user, empleado),
        num_rows="fixed",
        column_config={
            "KPI": st.column_config.TextColumn(
                "KPI",
                help="Nombre del KPI",
                width="large",
                disabled=True
            ),
            "Descripción": st.column_config.TextColumn(
                "Descripción",
                help="Descripción y forma de evaluar",
                width="large",
                disabled=True
            ),
            "Total": st.column_config.NumberColumn(
                "Total",
                help="Meta total del KPI",
                format="%d",
                step=1,
                width="small",
                disabled=not can_edit(st.session_state.user, empleado)
            ),
            "Cumplimiento": st.column_config.NumberColumn(
                "Cumplimiento",
                help="Valor alcanzado",
                format="%d",
                step=1,
                width="small",
                disabled=not can_edit(st.session_state.user, empleado)
            ),
            "Ponderación": st.column_config.NumberColumn(
                "Ponderación %",
                help="Porcentaje de ponderación",
                format="%d%%",
                width="small",
                disabled=True
            ),
            "Calificación": st.column_config.NumberColumn(
                "Calificación",
                help="(Resultado fórmula * Ponderación) / 100",
                format="%d%%",
                width="small",
                disabled=True
            ),
        },
        hide_index=True,
        column_order=["KPI", "Descripción", "Total", "Cumplimiento", "Ponderación", "Calificación"]
    )

    # Botón de evaluación
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("📊 Evaluar KPIs", type="primary", use_container_width=True):
            # Calcular resultado fórmula (en porcentaje entero)
            edited_df['Resultado fórmula'] = np.where(
                edited_df['Total'] != 0,
                ((edited_df['Cumplimiento'] / edited_df['Total'] * 100).round(0)).astype(int),
                0
            )
            
            # Calcular calificación (en porcentaje entero)
            edited_df['Calificación'] = ((edited_df['Resultado fórmula'] * edited_df['Ponderación'] / 100).round(0)).astype(int)
            
            # Actualizar datos en la sesión
            st.session_state.data = edited_df
            st.session_state.resultado_final = edited_df['Calificación'].sum()

    # Mostrar resultado final
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        st.metric(
            label="Resultado final de desempeño",
            value=f"{st.session_state.resultado_final}%",
            help="Suma total de todas las calificaciones"
        )

# Control de flujo principal
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    show_login()
else:
    show_main()

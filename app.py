import streamlit as st
import pandas as pd
import numpy as np
from users import login, get_accessible_departments, get_accessible_employees, can_edit, USERS, DEPARTAMENTOS

st.set_page_config(page_title="Sistema de Evaluación de KPIs", layout="wide")

# Guardar departamentos en session_state para acceso desde users.py
st.session_state.departamentos = DEPARTAMENTOS

# KPIs por departamento/persona
KPIS = {
    "Nayeli": {
        'KPI': ['KPI 1 Compras', 'KPI 2 Compras', 'KPI 3 Compras'],
        'Descripción': ['Descripción KPI 1', 'Descripción KPI 2', 'Descripción KPI 3'],
        'Total': [100, 100, 100],
        'Cumplimiento': [0, 0, 0],
        'Ponderación': [40, 30, 30]
    },
    # Agregar KPIs para cada empleado...
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
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# Función para mostrar la página principal
def show_main():
    st.title("Sistema de Evaluación de KPIs")
    
    # Mostrar información del usuario
    st.sidebar.markdown(f"""
    ### Usuario: {USERS[st.session_state.user]['name']}
    **Rol**: {USERS[st.session_state.user]['role'].replace('_', ' ').title()}
    **Departamento**: {USERS[st.session_state.user]['department'] or 'Todos los departamentos'}
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

    if not empleado:
        st.warning("No hay empleados disponibles para evaluar en este departamento.")
        return

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
    puede_editar = can_edit(st.session_state.user, empleado)
    edited_df = st.data_editor(
        st.session_state.data,
        key="editor",
        disabled=not puede_editar,
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
                disabled=not puede_editar
            ),
            "Cumplimiento": st.column_config.NumberColumn(
                "Cumplimiento",
                help="Valor alcanzado",
                format="%d",
                step=1,
                width="small",
                disabled=not puede_editar
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
        if st.button("📊 Evaluar KPIs", type="primary", use_container_width=True, disabled=not puede_editar):
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

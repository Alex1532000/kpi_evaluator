import streamlit as st
import pandas as pd
import numpy as np
from users import login, get_accessible_departments, get_accessible_employees, can_edit, USERS, DEPARTAMENTOS

st.set_page_config(
    page_title="Sistema de Evaluación de KPIs",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Estilos para la página de login */
    .login-container {
        display: flex;
        padding: 0;
        margin: 0;
        height: 100vh;
    }
    .image-section {
        flex: 2;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
    }
    .login-section {
        flex: 1;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background-color: white;
    }
    .login-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #2c5364;
        color: white;
        border: none;
        padding: 0.5rem;
        margin-top: 1rem;
    }
    .forgot-password {
        text-align: center;
        margin-top: 1rem;
        color: #666;
        font-size: 0.9rem;
    }
    .welcome-text {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: white;
    }
    .welcome-subtext {
        font-size: 1.2rem;
        color: #e0e0e0;
        margin-bottom: 2rem;
    }
    /* Iconos de evaluación */
    .evaluation-icons {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
    }
    .evaluation-icon {
        font-size: 3rem;
        color: white;
    }
    /* Ocultar el header por defecto de Streamlit en la página de login */
    [data-testid="stHeader"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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
    "Boris": {
        'KPI': [
            'Configuración de GPS - Cantidad',
            'Configuración de GPS - Éxito',
            'Pruebas de Funcionamiento',
            'Ensamblaje - Productos',
            'Ensamblaje - Accesorios',
            'Creación de Usuarios',
            'Creación de Unidades - Cantidad',
            'Creación de Unidades - Calidad'
        ],
        'Descripción': [
            'Cantidad total de GPS configurados según solicitudes',
            'Porcentaje de configuraciones exitosas del total realizado',
            'Número de equipos probados y verificados',
            'Cantidad de productos ensamblados según solicitudes',
            'Verificación del funcionamiento correcto de accesorios',
            'Cantidad de usuarios creados en plataformas según solicitudes',
            'Cantidad de unidades creadas en plataformas',
            'Porcentaje de unidades creadas sin errores en accesos empresariales'
        ],
        'Total': [100, 100, 100, 100, 100, 100, 100, 100],
        'Cumplimiento': [0, 0, 0, 0, 0, 0, 0, 0],
        'Ponderación': [15, 10, 15, 15, 10, 10, 15, 10]
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
    st.markdown("""
    <div class="login-container">
        <div class="image-section">
            <h1 class="welcome-text">Evaluación de Desempeño</h1>
            <p class="welcome-subtext">Sistema integral para la gestión y evaluación del rendimiento laboral</p>
            <div class="evaluation-icons">
                <div class="evaluation-icon">📊</div>
                <div class="evaluation-icon">📈</div>
                <div class="evaluation-icon">🎯</div>
            </div>
            <img src="https://img.freepik.com/free-vector/business-team-putting-together-jigsaw-puzzle-isolated-flat-vector-illustration-cartoon-partners-working-connection-teamwork-partnership-cooperation-concept_74855-9814.jpg" 
                 style="max-width: 80%; margin-top: 2rem; border-radius: 10px;">
        </div>
        <div class="login-section">
            <div class="login-box">
                <div class="login-header">
                    <h2>Iniciar Sesión</h2>
                    <p style="color: #666;">Ingrese sus credenciales para continuar</p>
                </div>
                <form>
                    <div style="margin-bottom: 1rem;">
                        <label style="color: #333;">Usuario</label>
                        <input type="text" id="username" 
                               style="width: 100%; padding: 0.5rem; margin-top: 0.5rem; border: 1px solid #ddd; border-radius: 4px;">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="color: #333;">Contraseña</label>
                        <input type="password" id="password" 
                               style="width: 100%; padding: 0.5rem; margin-top: 0.5rem; border: 1px solid #ddd; border-radius: 4px;">
                    </div>
                    <div style="display: flex; align-items: center; margin: 1rem 0;">
                        <input type="checkbox" id="remember" style="margin-right: 0.5rem;">
                        <label for="remember" style="color: #666;">Recordar mis credenciales</label>
                    </div>
                    <button type="submit" style="width: 100%; background-color: #2c5364; color: white; border: none; padding: 0.75rem; border-radius: 4px; cursor: pointer;">
                        Iniciar Sesión
                    </button>
                </form>
                <div class="forgot-password">
                    <a href="#" style="color: #2c5364; text-decoration: none;">¿Olvidó su contraseña?</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario real de Streamlit (oculto pero funcional)
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("", key="username_hidden", label_visibility="collapsed")
        password = st.text_input("", type="password", key="password_hidden", label_visibility="collapsed")
        submitted = st.form_submit_button("", type="primary")
        
        if submitted:
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

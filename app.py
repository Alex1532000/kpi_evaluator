import streamlit as st
import pandas as pd
import numpy as np
from users import login, get_accessible_departments, get_accessible_employees, can_edit, USERS, DEPARTAMENTOS
import io
from datetime import datetime

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
    "Eduardo": {
        'KPI': [
            'Entregas a tiempo',
            'Diseños aprobados',
            'Materiales diseñados',
            'Interacción en redes',
            'Manual de marca',
            'Satisfacción interna',
            'Errores post-publicación',
            'Contenidos publicados',
            'Impacto en redes',
            'Innovación visual',
            'Colaboración',
            'Tiempo de respuesta'
        ],
        'Descripción': [
            'Fechas de entrega planificadas vs reales; se califica el cumplimiento de los plazos',
            'Número de diseños aceptados sin corrección; se califica la precisión y alineación con el briefing',
            'Volumen de trabajo entregado; se califica la productividad mensual',
            'Número de likes, comentarios y compartidos en relación a las impresiones; se califica la efectividad del diseño en redes',
            'Revisión de cumplimiento con los lineamientos del manual de marca; se califica consistencia visual',
            'Promedio de satisfacción de equipos internos en cuanto a calidad y tiempos; se califica percepción interna',
            'Cantidad y tipo de errores visuales detectados tras publicación; se califica nivel de revisión previa',
            'Cantidad de contenidos que efectivamente fueron publicados; se califica impacto y efectividad del trabajo entregado',
            'Comparación del CTR visual o alcance con el promedio; se califica relevancia del contenido',
            'Cantidad de piezas innovadoras (nuevos estilos, formatos); se califica creatividad e innovación',
            'Resultados de encuestas sobre colaboración y comunicación; se califica el trabajo en equipo',
            'Horas promedio desde solicitud hasta respuesta inicial; se califica nivel de respuesta y atención'
        ],
        'Total': [1, 10, 10, 50, 10, 10, 10, 10, 100, 5, 5, 4],
        'Cumplimiento': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Ponderación': [10, 10, 8, 8, 8, 10, 8, 8, 8, 7, 7, 8]
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

# Función para exportar KPIs individuales a Excel
def export_individual_kpis(empleado, departamento, fecha, df_kpis):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('KPIs')
    
    # Formato para títulos
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'left',
        'bg_color': '#2c5364',
        'font_color': 'white'
    })
    
    # Formato para subtítulos
    subheader_format = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'align': 'left',
        'bg_color': '#203a43'
    })
    
    # Formato para datos
    data_format = workbook.add_format({
        'font_size': 10,
        'align': 'left'
    })
    
    # Escribir encabezado
    worksheet.write(0, 0, f"Evaluación de KPIs - {empleado}", header_format)
    worksheet.write(1, 0, f"Departamento: {departamento}", data_format)
    worksheet.write(2, 0, f"Fecha de evaluación: {fecha.strftime('%d/%m/%Y')}", data_format)
    
    # Escribir descripción general
    worksheet.write(4, 0, "Descripción de la evaluación:", subheader_format)
    worksheet.write(5, 0, "Evaluación mensual de indicadores clave de desempeño (KPIs) que miden la eficiencia, calidad y cumplimiento de objetivos.", data_format)
    
    # Escribir KPIs
    worksheet.write(7, 0, "Detalle de KPIs", subheader_format)
    
    # Encabezados de la tabla
    columns = ['KPI', 'Descripción', 'Meta', 'Cumplimiento', 'Ponderación', 'Calificación']
    for col, header in enumerate(columns):
        worksheet.write(8, col, header, header_format)
    
    # Datos de KPIs
    for row, (index, kpi_row) in enumerate(df_kpis.iterrows(), start=9):
        worksheet.write(row, 0, kpi_row['KPI'], data_format)
        worksheet.write(row, 1, kpi_row['Descripción'], data_format)
        worksheet.write(row, 2, kpi_row['Total'], data_format)
        worksheet.write(row, 3, kpi_row['Cumplimiento'], data_format)
        worksheet.write(row, 4, f"{kpi_row['Ponderación']}%", data_format)
        if 'Calificación' in df_kpis.columns:
            worksheet.write(row, 5, f"{kpi_row['Calificación']}%", data_format)
    
    # Ajustar anchos de columna
    worksheet.set_column(0, 0, 30)  # KPI
    worksheet.set_column(1, 1, 50)  # Descripción
    worksheet.set_column(2, 5, 15)  # Otras columnas
    
    writer.close()
    return output.getvalue()

# Función para exportar resumen global de KPIs
def export_global_kpis():
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Resumen Global')
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'left',
        'bg_color': '#2c5364',
        'font_color': 'white'
    })
    
    data_format = workbook.add_format({
        'font_size': 10,
        'align': 'left'
    })
    
    # Encabezado
    fecha_actual = datetime.now().strftime('%d/%m/%Y')
    worksheet.write(0, 0, f"Resumen Global de KPIs - {fecha_actual}", header_format)
    
    # Encabezados de columnas
    columns = ['Colaborador', 'Departamento', 'Calificación Total']
    for col, header in enumerate(columns):
        worksheet.write(2, col, header, header_format)
    
    # Recopilar datos de todos los colaboradores
    row = 3
    for dept, empleados in DEPARTAMENTOS.items():
        for empleado in empleados:
            if empleado.lower().replace(" ", "") in KPIS:
                kpi_data = KPIS[empleado.lower().replace(" ", "")]
                # Calcular calificación total
                total = sum([
                    (min(cum/tot*100, 100) if tot != 0 else 0) * pond/100
                    for cum, tot, pond in zip(
                        kpi_data['Cumplimiento'],
                        kpi_data['Total'],
                        kpi_data['Ponderación']
                    )
                ])
                
                worksheet.write(row, 0, empleado, data_format)
                worksheet.write(row, 1, dept, data_format)
                worksheet.write(row, 2, f"{total:.1f}%", data_format)
                row += 1
    
    # Ajustar anchos de columna
    worksheet.set_column(0, 0, 30)  # Colaborador
    worksheet.set_column(1, 1, 30)  # Departamento
    worksheet.set_column(2, 2, 20)  # Calificación Total
    
    writer.close()
    return output.getvalue()

# Función para mostrar la página principal
def show_main():
    st.title("Sistema de Evaluación de KPIs")
    
    # Mostrar información del usuario y botones de exportación en el sidebar
    st.sidebar.markdown(f"""
    ### Usuario: {USERS[st.session_state.user]['name']}
    **Rol**: {USERS[st.session_state.user]['role'].replace('_', ' ').title()}
    **Departamento**: {USERS[st.session_state.user]['department'] or 'Todos los departamentos'}
    """)
    
    # Botón de exportación global (solo para administradores)
    if USERS[st.session_state.user]['role'] in ['super_admin', 'admin']:
        if st.sidebar.button("📊 Exportar Resumen Global"):
            excel_data = export_global_kpis()
            st.sidebar.download_button(
                label="⬇️ Descargar Resumen Global",
                data=excel_data,
                file_name=f"resumen_global_kpis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
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
        fecha_eval = st.date_input("Mes de evaluación", key="fecha_evaluacion")

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

    # Botones de evaluación y exportación
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
    
    with col3:
        if st.button("📑 Exportar KPIs", use_container_width=True):
            excel_data = export_individual_kpis(empleado, departamento, fecha_eval, edited_df)
            st.download_button(
                label="⬇️ Descargar Reporte",
                data=excel_data,
                file_name=f"kpis_{empleado}_{fecha_eval.strftime('%Y%m')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

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

import streamlit as st
from typing import Dict, List

# Definición de roles y sus permisos
ROLES = {
    "super_admin": {
        "description": "Acceso total al sistema como propietario",
        "can_view_all": True,
        "can_edit_all": True
    },
    "admin": {
        "description": "Acceso administrativo con restricciones específicas",
        "can_view_all": True,
        "can_edit_specific": True
    },
    "coordinador": {
        "description": "Puede ver y evaluar su área y subordinados",
        "can_view_all": False,
        "can_edit_specific": True
    },
    "encargado": {
        "description": "Puede ver y evaluar sus subordinados directos",
        "can_view_all": False,
        "can_edit_specific": True
    },
    "empleado": {
        "description": "Solo puede ver su propia evaluación",
        "can_view_all": False,
        "can_edit_all": False
    }
}

# Usuarios del sistema
USERS = {
    "admin": {
        "password": "admin2024",
        "role": "super_admin",
        "name": "Super Administrador",
        "department": None,
        "can_evaluate": "all"  # Puede evaluar a todos
    },
    "cesar": {
        "password": "cesar2024",
        "role": "admin",
        "name": "Cesar",
        "department": None,
        "can_evaluate": "all"  # Puede evaluar a todos
    },
    "lucia": {
        "password": "lucia2024",
        "role": "admin",
        "name": "Lucia",
        "department": None,
        "can_evaluate": ["nayeli", "mariana", "pablo", "octavio", "oscar"]
    },
    "alejandro": {
        "password": "alejandro2024",
        "role": "coordinador",
        "name": "Alejandro Muñiz",
        "department": "Laboratorio",
        "can_evaluate": ["boris", "eduardo", "nuevo_programador"]
    },
    "enrique": {
        "password": "enrique2024",
        "role": "encargado",
        "name": "Enrique",
        "department": "Área Técnica",
        "can_evaluate": ["jesus_lopez", "eduardo_tec", "alejandro_tec", "alva", "david", "gustavo"]
    },
    "brenda": {
        "password": "brenda2024",
        "role": "encargado",
        "name": "Brenda",
        "department": "Soporte de Plataforma",
        "can_evaluate": ["jesus_dominguez", "susana", "karla", "marco"]
    },
    "marine": {
        "password": "marine2024",
        "role": "empleado",
        "name": "Marine",
        "department": "Contraloría",
        "can_evaluate": []
    },
    "abraham": {
        "password": "abraham2024",
        "role": "empleado",
        "name": "Abraham",
        "department": "Auxiliar",
        "can_evaluate": []
    }
}

# Lista completa de empleados por departamento
DEPARTAMENTOS = {
    "Compras": ["Nayeli"],
    "Cobranza": ["Mariana"],
    "Ventas": ["Pablo", "Octavio"],
    "Capacitaciones y Calidad": ["Oscar"],
    "Hardware": ["Boris"],
    "Diseño": ["Eduardo"],
    "Programación": ["Nuevo Programador"],
    "Área Técnica": ["Jesus Lopez", "Eduardo Tec", "Alejandro Tec", "Alva", "David", "Gustavo"],
    "Soporte de Plataforma": ["Jesus Dominguez", "Susana", "Karla", "Marco"],
    "Contraloría": ["Marine"],
    "Auxiliar": ["Abraham"]
}

def login(username: str, password: str) -> bool:
    """Verifica las credenciales del usuario."""
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.user = username
        st.session_state.role = USERS[username]["role"]
        st.session_state.department = USERS[username]["department"]
        st.session_state.can_evaluate = USERS[username]["can_evaluate"]
        return True
    return False

def get_accessible_departments(username: str) -> List[str]:
    """Obtiene los departamentos a los que tiene acceso el usuario."""
    if username not in USERS:
        return []
    
    user = USERS[username]
    role = user["role"]
    
    if role in ["super_admin", "admin"]:
        return list(DEPARTAMENTOS.keys())
    
    if user["department"]:
        accessible_depts = [user["department"]]
        # Agregar departamentos de los empleados que puede evaluar
        for dept, empleados in DEPARTAMENTOS.items():
            if any(emp.lower().replace(" ", "_") in user["can_evaluate"] for emp in empleados):
                if dept not in accessible_depts:
                    accessible_depts.append(dept)
        return accessible_depts
    
    return []

def get_accessible_employees(username: str, department: str) -> List[str]:
    """Obtiene los empleados que puede ver/evaluar el usuario."""
    if username not in USERS:
        return []
    
    user = USERS[username]
    role = user["role"]
    
    if role == "super_admin" or user["can_evaluate"] == "all":
        return DEPARTAMENTOS.get(department, [])
    
    if department in DEPARTAMENTOS:
        return [emp for emp in DEPARTAMENTOS[department] 
                if emp.lower().replace(" ", "_") in user["can_evaluate"]]
    
    return []

def can_edit(username: str, employee: str) -> bool:
    """Verifica si el usuario puede editar la evaluación del empleado."""
    if username not in USERS:
        return False
    
    user = USERS[username]
    
    if user["role"] == "super_admin" or user["can_evaluate"] == "all":
        return True
    
    return employee.lower().replace(" ", "_") in user["can_evaluate"]

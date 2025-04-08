import streamlit as st
from typing import Dict, List

# Definición de roles y sus permisos
ROLES = {
    "admin": {
        "description": "Acceso total al sistema",
        "can_view_all": True,
        "can_edit_all": True
    },
    "director": {
        "description": "Puede ver todos los departamentos",
        "can_view_all": True,
        "can_edit_all": False
    },
    "encargado": {
        "description": "Puede ver y evaluar su departamento",
        "can_view_all": False,
        "can_edit_all": False
    }
}

# Usuarios del sistema
USERS = {
    "admin": {
        "password": "admin2024",
        "role": "admin",
        "name": "Administrador",
        "department": None  # Puede ver todos los departamentos
    },
    "director": {
        "password": "director2024",
        "role": "director",
        "name": "Director General",
        "department": None  # Puede ver todos los departamentos
    },
    "alejandro": {
        "password": "coord2024",
        "role": "encargado",
        "name": "Alejandro Muñiz",
        "department": "Coordinación Laboratorio",
        "manages": ["Otros"]
    },
    "boris": {
        "password": "hw2024",
        "role": "encargado",
        "name": "Boris Gonzalez",
        "department": "Hardware",
        "manages": []
    },
    "oscar": {
        "password": "dev2024",
        "role": "encargado",
        "name": "Oscar Ramirez",
        "department": "Programación",
        "manages": ["Ivan N.", "Nuevo"]
    }
}

def login(username: str, password: str) -> bool:
    """Verifica las credenciales del usuario."""
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.user = username
        st.session_state.role = USERS[username]["role"]
        st.session_state.department = USERS[username]["department"]
        st.session_state.manages = USERS[username].get("manages", [])
        return True
    return False

def get_accessible_departments(username: str) -> List[str]:
    """Obtiene los departamentos a los que tiene acceso el usuario."""
    if username not in USERS:
        return []
    
    user = USERS[username]
    role = user["role"]
    
    if ROLES[role]["can_view_all"]:
        return list(st.session_state.departamentos.keys())
    
    if user["department"]:
        return [user["department"]]
    
    return []

def get_accessible_employees(username: str, department: str) -> List[str]:
    """Obtiene los empleados que puede ver/evaluar el usuario."""
    if username not in USERS:
        return []
    
    user = USERS[username]
    role = user["role"]
    
    if ROLES[role]["can_view_all"]:
        return st.session_state.departamentos.get(department, [])
    
    if department == user["department"]:
        return user.get("manages", []) + [user["name"]]
    
    return []

def can_edit(username: str, employee: str) -> bool:
    """Verifica si el usuario puede editar la evaluación del empleado."""
    if username not in USERS:
        return False
    
    user = USERS[username]
    role = user["role"]
    
    if ROLES[role]["can_edit_all"]:
        return True
    
    return employee in user.get("manages", [])

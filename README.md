<p align="center">
  <img src="images/gestor_de_videojuegos.png" alt="Gestor de Videojuegos Banner" width="800">
</p>

# 🎮 Gestor de Videojuegos — Proyecto en Python 🐍  

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite" alt="SQLite Badge">
  <img src="https://img.shields.io/badge/ORM-SQLAlchemy-red?logo=python" alt="SQLAlchemy Badge">
</p>

---

## 🕹️ Descripción del proyecto  

**Gestor de Videojuegos** es una aplicación desarrollada en **Python** que permite administrar una base de datos con información sobre distintos títulos, géneros, plataformas y valoraciones.  

El proyecto combina la gestión de datos mediante **SQLite** y **SQLAlchemy** con los principios de la **Programación Orientada a Objetos (POO)**, ofreciendo una estructura modular, escalable y fácil de mantener.  

---

## 🎯 Objetivos principales  

- 📂 Registrar y almacenar videojuegos en una base de datos local  
- 🕹️ Consultar y mostrar información detallada de los juegos  
- 🔍 Filtrar títulos por género, plataforma o clasificación  
- 🧩 Aplicar buenas prácticas de **POO** y diseño de clases  

Este trabajo forma parte del curso **Python + IA**, y tiene como finalidad reforzar nuestras habilidades en programación y trabajo en equipo.  

---

## 👥 Equipo de desarrollo  

| Integrantes
|------------- 
| Paco Gutiérrez Frías 
| Lueyo Suárez González 
| Jon Fernandes Aizcorbe

---

## ⚙️ Tecnologías utilizadas  

- 🐍 **Python 3**  
- 🗃️ **SQLite** (Base de datos local)  
- 🔗 **SQLAlchemy** (ORM para gestión de datos)  
- 🧠 **Programación Orientada a Objetos (POO)**  

---

## 🚀 Ejecución e instalación  

> 📌 **Nota:** Las instrucciones detalladas se publicarán próximamente cuando el proyecto alcance su versión funcional inicial.

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/Mapakitus/gestor-videojuegos.git


---

## [OK] mover rama lueyo
## [OK] resetear main:
  Opción 1: deshacer ultimos 8 commits:
   - git reset --hard HEAD~8
   - git push --force
  Opción 2:
    -manualmente colocar todo a un estado deseado
## GESTOR VIDEOJUEGOS (ENTIDADES)

## Videojuego # (ManyToOne con Genero, ManyToOne Desarrolladora) (Paco)

## Genero (Jon)

## Desarroladora (Lueyo)

## Usuario (Lueyo)
- id
- email
- nif
- password
- saldo

## Review # (ManyToOne Videojuego, ManyToOne Usuario)

## Compra # (ManyToOne Videojuego, ManyToOne Usuario)

## Schemas pydantic
  - API REST CRUD
  - HTMLs

## Opcional autenticación:
- registro.html
- login.html
- lógica para detectar el usuario autenticado en los controladores
- opción simple: no hacer registro ni login, simplemente tener un usuario en base datos y vincular cada operación de Review o Compra a ese usuario


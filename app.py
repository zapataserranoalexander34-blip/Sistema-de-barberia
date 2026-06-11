#importar las librerias
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime

#conexion a la base de datos
URI = 'mongodb+srv://alexzs:Alex270809@cluster0.6yljwda.mongodb.net/?appName=Cluster0'

client = MongoClient(URI)

# Base de datos
db = client["Barberia"]

# Colecciones
colecciones = {
    "Hombres": db["Hombres"],
    "Mujeres": db["Mujeres"],
    "Niños": db["Niños"]
}

# Configuración de la página
st.set_page_config(
    page_title="Sistema De Barbería",
    page_icon="💈",
    layout="wide"
)

st.title("💈 Sistema de Gestión de Barbería")

# Menú lateral
opcion = st.sidebar.selectbox(
    "Seleccione una colección",
    list(colecciones.keys())
)

coleccion = colecciones[opcion]

# Operaciones CRUD
accion = st.sidebar.radio(
    "Opción",
    ["Agregar", "Consultar", "Actualizar", "Gráfica"]
)

# ==================================================
# AGREGAR
# ==================================================
if accion == "Agregar":

    st.write("Agregar registro a opccion:", opcion)

    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", 0, 100, 18)
    telefono = st.text_input("Teléfono")

    if opcion in ["Barberos", "Estilistas"]:
        especialidad = st.text_input("Especialidad")
    else:
        especialidad = ""

    if st.button("Guardar"):

        documento = {
            "nombre": nombre,
            "edad": edad,
            "telefono": telefono,
            "fecha_registro": datetime.now()
        }

        if especialidad:
            documento["especialidad"] = especialidad

        resultado = coleccion.insert_one(documento)

        st.success(
            f"Registro agregado correctamente. ID: {resultado.inserted_id}"
        )

# ==================================================
# CONSULTAR
# ==================================================
elif accion == "Consultar":

    st.write("Registros de:", opcion)

    datos = list(coleccion.find())

    if datos:

        for dato in datos:
            dato["_id"] = str(dato["_id"])

        df = pd.DataFrame(datos)
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No existen registros.")

# ==================================================
# ACTUALIZAR
# ==================================================
elif accion == "Actualizar":

    st.write("Actualizar registro en:", opcion)

    datos = list(coleccion.find())

    if datos:

        ids = [str(doc["_id"]) for doc in datos]

        id_seleccionado = st.selectbox(
            "Seleccione un ID",
            ids
        )

        documento = coleccion.find_one(
            {"_id": ObjectId(id_seleccionado)}
        )

        nombre = st.text_input(
            "Nombre",
            documento.get("nombre", "")
        )

        edad = st.number_input(
            "Edad",
            0,
            100,
            int(documento.get("edad", 0))
        )

        telefono = st.text_input(
            "Teléfono",
            documento.get("telefono", "")
        )

        if opcion in ["Barberos", "Estilistas"]:
            especialidad = st.text_input(
                "Especialidad",
                documento.get("especialidad", "")
            )
        else:
            especialidad = ""

        if st.button("Actualizar"):

            nuevos_datos = {
                "nombre": nombre,
                "edad": edad,
                "telefono": telefono
            }

            if especialidad:
                nuevos_datos["especialidad"] = especialidad

            coleccion.update_one(
                {"_id": ObjectId(id_seleccionado)},
                {"$set": nuevos_datos}
            )

            st.success("Registro actualizado correctamente.")

    else:
        st.warning("No existen registros para actualizar.")

# ==================================================
# GRÁFICA
# ==================================================
elif accion == "Gráfica":

    st.subheader(f"📊 Gráfica de edades - {opcion}")

    datos = list(coleccion.find())

    if datos:

        for dato in datos:
            dato["_id"] = str(dato["_id"])

        df = pd.DataFrame(datos)

        if "edad" in df.columns:

            st.bar_chart(
                df["edad"].value_counts().sort_index()
            )

            st.write("Distribución de edades")
            st.dataframe(
                df[["nombre", "edad"]],
                use_container_width=True
            )

        else:
            st.warning("No existe el campo edad.")

    else:
        st.warning("No existen registros para graficar.")

# ==================================================
# PIE DE PÁGINA
# ==================================================
st.sidebar.markdown("---")
st.sidebar.info("Sistema Barbería - Streamlit + MongoDB")

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from xhtml2pdf import pisa
import streamlit as st
from streamlit_quill import st_quill
from datetime import date

def main():
    st.title("Generador de CV")
    fecha_minima = date(1950, 1, 1)
    fecha_maxima = date.today()
    #Barra de herramientas customizadas para ST_QUILL
    custom_toolbar = [{'list':'bullet'}]
    #Datos Básicos
    st.header("Información Personal")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Email")
    with col2:
        teléfono = st.text_input("Teléfono")
        links = st.text_input("LinkedIn o Potafolio")
    direccion = st.text_input("Dirección")
    perfil = st.text_area("Perfil")

    #Experiencia
    st.header("Experiencia Laboral")

    #Contador para experiencia
    if 'num_experiencia' not in st.session_state:
        st.session_state.num_experiencia = 1

    #Campos para experiencia
    for i in range(st.session_state.num_experiencia):
        with st.expander(f"Experiencia #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Puesto", key=f"puesto_{i}")
                st.date_input(f"Inicio", key=f"inicio_{i}",format="DD/MM/YYYY",min_value=fecha_minima,max_value=fecha_maxima)
            with col2:
                st.text_input(f"Empresa", key=f"empresa_{i}")
                st.date_input(f"Fin", key=f"fin_{i}",format="DD/MM/YYYY",min_value=fecha_minima,max_value=fecha_maxima)
            st.text("Tareas y logros")
            st_quill(key=f"tareas_{i}",toolbar=custom_toolbar)
            
    if st.button("➕ Agregar Experiencia"):
        st.session_state.num_experiencia += 1
        st.rerun()

    #Contador para educación
    st.header("Educación")
    if 'num_educacion' not in st.session_state:
        st.session_state.num_educacion = 1

    #Campos para educación
    for i in range(st.session_state.num_educacion):
        with st.expander(f"Educación #{i+1}", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input(f"Titulo", key=f"titulo_{i}")
            with col2:
                st.text_input(f"Institución", key=f"institucion_{i}")
            with col3:
                st.date_input(f"Fecha", key=f"anio_{i}",format="DD/MM/YYYY",min_value=fecha_minima,max_value=fecha_maxima)
                #st.text_input(f"Año", key=f"anio_{i}")
   
    if st.button("➕ Agregar Educación"):
        st.session_state.num_educacion += 1
        st.rerun()

    #Contador para idiomas
    st.header("Idiomas")
    if 'num_idioma' not in st.session_state:
        st.session_state.num_idioma = 1
    
    #Campos para idioma
    for i in range(st.session_state.num_idioma):
        with st.expander(f"Idioma #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Idioma", key=f"idioma_{i}")
            with col2:
                option = st.selectbox('Seleccione su nivel:',
                    ('Principiante', 'Intermedio', 'Avanzado', 'Nativo'), index=0,key=f"nivel_{i}")
   
    if st.button("➕ Agregar Idioma"):
        st.session_state.num_idioma += 1
        st.rerun()

    #Contador para Certificaciones
    st.header("Certificaciones")
    if 'num_cert' not in st.session_state:
        st.session_state.num_cert = 1
    
    #Campos para idioma
    for i in range(st.session_state.num_cert):
        with st.expander(f"Certificación #{i+1}", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input(f"Certificación", key=f"cert_{i}")
            with col2:
                st.text_input(f"Institución", key=f"inst_{i}")
            with col3:
                st.date_input(f"Fecha", key=f"anio_cert_{i}",format="DD/MM/YYYY",min_value=fecha_minima,max_value=fecha_maxima)
   
    if st.button("➕ Agregar Certificación"):
        st.session_state.num_cert += 1
        st.rerun()

    #Contador para Categoría de Habilidades
    st.header("Habilidades")
    if 'num_hab' not in st.session_state:
        st.session_state.num_hab = 1

    #Campos para habilidades
    for i in range(st.session_state.num_hab):
        with st.expander(f"Categoría de habilidades #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Categoría", key=f"cat_{i}")
            with col2:
                st.text_input(f"Habilidades (separadas por , )", key=f"hab_{i}")
    
    if st.button("➕ Agregar Categoría de Habilidades"):
        st.session_state.num_hab += 1
        st.rerun()

    #-------------------------Generación de PDF-------------------------

    lista_experiencia = [
    {
        "Puesto": st.session_state.get(f"puesto_{i}", ""),
        "Empresa": st.session_state.get(f"empresa_{i}", ""),
        "Inicio": st.session_state.get(f"inicio_{i}", ""),
        "Fin": st.session_state.get(f"fin_{i}", ""),
        "Tareas y logros": "<br/>".join([f"• {linea.strip()}"for linea in str(st.session_state.get(f"tareas_{i}", "")).split("\n") if linea.strip()])
    }
    for i in range(st.session_state.num_experiencia)]


    lista_educacion = [
        {
            "Titulo": st.session_state[f"titulo_{i}"],
            "Año": st.session_state[f"anio_{i}"],
            "Institución": st.session_state[f"institucion_{i}"]
        }
        for i in range(st.session_state.num_educacion)]
        
    lista_idiomas = [
        {
            "Idioma": st.session_state[f"idioma_{i}"],
            "Nivel": st.session_state[f"nivel_{i}"]
        }
        for i in range(st.session_state.num_idioma)]
    
    lista_certificaciones = [
        {
            "Certificación": st.session_state[f"cert_{i}"],
            "Institución": st.session_state[f"inst_{i}"], 
            "Año": st.session_state[f"anio_cert_{i}"]
        }
        for i in range(st.session_state.num_cert)]
    
    lista_habilidades = [
        {
            "Categoría": st.session_state[f"cat_{i}"],
            "Habilidades": st.session_state[f"hab_{i}"]
        }
        for i in range(st.session_state.num_hab)]
        
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = []
    
    # Estilos personalizados para claridad
    formato_nombre = ParagraphStyle('Nombre', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=18, spaceAfter=5)
    formato_contacto = ParagraphStyle('Contacto', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, spaceAfter=6)
    formato_contenido = ParagraphStyle('Contenido', parent=styles['Normal'], alignment=TA_JUSTIFY, fontSize=10, spaceAfter=12)
    formato_seccion = ParagraphStyle('Seccion', parent=styles['Heading2'], fontSize=12, spaceBefore=10, spaceAfter=1, borderPadding=2)

    division = HRFlowable(width="100%", thickness=1, color="black", spaceAfter=10)
    division_light = HRFlowable(width="100%", thickness=0.3, color="grey", spaceAfter=20)
    
    titulo = Paragraph(f'{nombre}', formato_nombre)
    contacto = Paragraph(f"{direccion} | {email} | {teléfono} | {links}", formato_contacto)
    perfil_profesional = Paragraph(f"{perfil}",formato_contenido)

    elementos.append(titulo)
    elementos.append(contacto)
    elementos.append(division_light)

    elementos.append(Paragraph("PERFIL", formato_seccion))
    elementos.append(division)
    elementos.append(perfil_profesional)
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("EXPERIENCIA", formato_seccion))
    elementos.append(division)  
    for item in lista_experiencia:
        elementos.append(Paragraph(f"<b>{item['Puesto']}</b> en {item['Empresa']} | {item['Inicio']} - {item['Fin']}"))
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"{item['Tareas y logros']}",formato_contenido))
        elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("EDUCACIÓN", formato_seccion))
    elementos.append(division)
    for item in lista_educacion:
        elementos.append(Paragraph(f"<b>{item['Titulo']}</b> - {item['Institución']} - {item['Año']}"))
        elementos.append(Spacer(1, 10))   
    elementos.append(Spacer(1, 15))

    elementos.append(Paragraph("IDIOMAS", formato_seccion))
    elementos.append(division)
    for item in lista_idiomas:
        elementos.append(Paragraph(f"<b>{item['Idioma']}:</b> {item['Nivel']}"))

    elementos.append(Paragraph("CERTIFICACIONES", formato_seccion))
    elementos.append(division)
    for item in lista_certificaciones:
        elementos.append(Paragraph(f"<b>{item['Certificación']}</b> - {item['Institución']} - {item['Año']}"))

    elementos.append(Paragraph("HABILIDADES", formato_seccion))
    elementos.append(division)
    for item in lista_habilidades:
        elementos.append(Paragraph(f"<b>{item['Categoría']}:</b> {item['Habilidades']}"))
            
    doc.build(elementos)
    pdf_final = buffer.getvalue()

    if st.download_button(label="📥 Descargar CV PDF",data=pdf_final,file_name=f"CV_{nombre}.pdf",mime="application/pdf"):
        st.success(f"¡CV de {nombre} listo para descargar!")

if __name__ == "__main__":
    main()



 



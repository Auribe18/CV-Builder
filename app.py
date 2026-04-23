from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from io import BytesIO
import streamlit as st
from streamlit_quill import st_quill
from datetime import date
import html

def main():
    with st.sidebar:
         st.header("💡 Tips & Tricks")
         st.markdown("""
    ### 1. Formato de Texto
    Puedes usar estas etiquetas en tus **Tareas y Logros** para resaltar información:
    * `<b>Texto</b>` → **Negrita** (Úsalo para KPIs).
    * `<i>Texto</i>` → *Cursiva*.
    * `<u>Texto</u>` → <u>Subrayado</u>.
    
    ---
    ### 2. Enfoque en Logros
    Los reclutadores buscan resultados, no solo tareas.
    * **Tip:** Intenta usar la fórmula: *Logré X, medido por Y, haciendo Z.*
    
    ---
    ### 3. Keywords ATS
    Usa términos técnicos exactos (ej. **SAP BTP**, **Python**, **RPA**) para que los filtros te encuentren fácilmente.
    
    ---
    ### 4. Privacidad
    Esta herramienta **no almacena tus datos**. El documento se genera localmente en tu navegador.
    """)
    st.title("Generador de CV")
    esc = html.escape
    fecha_minima = date(1950, 1, 1)
    fecha_maxima = date.today()
    #Barra de herramientas customizadas para ST_QUILL
    custom_toolbar = [{'list':'bullet'}]
    #Datos Básicos
    st.header("Información Personal")
    col1, col2 = st.columns(2)
    with col1:
        nombre = esc(st.text_input("Nombre completo"))
        email = esc(st.text_input("Email"))
    with col2:
        teléfono = esc(st.text_input("Teléfono"))
        links = esc(st.text_input("LinkedIn o Potafolio"))
    direccion = esc(st.text_input("Dirección"))
    perfil = esc(st.text_area("Perfil")).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>').replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>').replace('&lt;u&gt;', '<u>').replace('&lt;/u&gt;', '</u>')

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

    # --- EXPERIENCIA ---
    lista_experiencia = [
        {
            "Puesto": esc(st.session_state.get(f"puesto_{i}", "")),
            "Empresa": esc(st.session_state.get(f"empresa_{i}", "")),
            "Inicio": st.session_state[f"inicio_{i}"].strftime("%b %Y") if st.session_state.get(f"inicio_{i}") else "",
            "Fin": st.session_state[f"fin_{i}"].strftime("%b %Y") if st.session_state.get(f"fin_{i}") else "Presente",
            "Tareas y logros": "<br/>".join([
                f"• {esc(linea.strip()).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>').replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>').replace('&lt;u&gt;', '<u>').replace('&lt;/u&gt;', '</u>')}"
                for linea in str(st.session_state.get(f"tareas_{i}", "")).split("\n") 
                if linea.strip()
            ])
        }
        for i in range(st.session_state.num_experiencia)
    ]

    # --- EDUCACIÓN ---
    lista_educacion = [
        {
            "Titulo": esc(st.session_state.get(f"titulo_{i}", "")),
            "Año": st.session_state[f"anio_{i}"].strftime("%b %Y") if st.session_state.get(f"anio_{i}") else "",
            "Institución": esc(st.session_state.get(f"institucion_{i}", ""))
        }
        for i in range(st.session_state.num_educacion)
    ]

    # --- IDIOMAS ---
    lista_idiomas = [
        {
            "Idioma": esc(st.session_state.get(f"idioma_{i}", "")),
            "Nivel": esc(st.session_state.get(f"nivel_{i}", ""))
        }
        for i in range(st.session_state.num_idioma)
    ]

    # --- CERTIFICACIONES ---
    lista_certificaciones = [
        {
            "Certificación": esc(st.session_state.get(f"cert_{i}", "")),
            "Institución": esc(st.session_state.get(f"inst_{i}", "")), 
            "Año": st.session_state[f"anio_cert_{i}"].strftime("%b %Y") if st.session_state.get(f"anio_cert_{i}") else ""
        }
        for i in range(st.session_state.num_cert)
    ]

    # --- HABILIDADES ---
    lista_habilidades = [
        {
            "Categoría": esc(st.session_state.get(f"cat_{i}", "")),
            "Habilidades": esc(st.session_state.get(f"hab_{i}", ""))
        }
        for i in range(st.session_state.num_hab)
    ]
  
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = []
    
    # Estilos personalizados para claridad
    COLOR_TITULO = HexColor('#2C3E50')  # Gris azulado 
    COLOR_LINEA = HexColor('#BDC3C7')   # Gris claro

    formato_nombre = ParagraphStyle(
        'Nombre', 
        parent=styles['Heading1'], 
        alignment=TA_CENTER, 
        fontSize=18, 
        spaceAfter=5)
    formato_contacto = ParagraphStyle(
        'Contacto', 
        parent=styles['Normal'], 
        alignment=TA_CENTER, 
        fontSize=10, 
        spaceAfter=6)
    formato_contenido = ParagraphStyle(
        'Contenido', 
        parent=styles['Normal'], 
        alignment=TA_JUSTIFY, 
        fontSize=10,
        leading=14,
        textColor=HexColor('#34495E'),  # Gris oscuro para el texto 
        spaceAfter=12)
    formato_seccion = ParagraphStyle(
        'Seccion', 
        parent=styles['Heading2'], 
        fontSize=11,
        textColor=COLOR_TITULO, 
        spaceBefore=15, 
        spaceAfter=8,
        fontName="Helvetica-Bold",
        textTransform="uppercase",
        letterSpacing=1)
    division = HRFlowable(
        width="100%", 
        thickness=0.5, 
        color=COLOR_LINEA, 
        spaceAfter=10)
    division_light = HRFlowable(
        width="100%", 
        thickness=0.3, 
        color=COLOR_LINEA, 
        spaceAfter=10)
    
    titulo = Paragraph(f'{nombre}', formato_nombre)
    contacto = Paragraph(f"{direccion} | {email} | {teléfono} | <link>{links}</link>", formato_contacto)
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
        elementos.append(Paragraph(f"<b>{item['Titulo']}</b> - {item['Institución']} | {item['Año']}"))  
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("IDIOMAS", formato_seccion))
    elementos.append(division)
    for item in lista_idiomas:
        elementos.append(Paragraph(f"<b>{item['Idioma']}:</b> {item['Nivel']}"))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("CERTIFICACIONES", formato_seccion))
    elementos.append(division)
    for item in lista_certificaciones:
        elementos.append(Paragraph(f"<b>{item['Certificación']}</b> - {item['Institución']} | {item['Año']}"))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("HABILIDADES", formato_seccion))
    elementos.append(division)
    for item in lista_habilidades:
        elementos.append(Paragraph(f"<b>{item['Categoría']}:</b> {item['Habilidades']}"))
    elementos.append(Spacer(1, 10))     
    doc.build(elementos)
    pdf_final = buffer.getvalue()

    if st.download_button(label="📥 Descargar CV PDF",data=pdf_final,file_name=f"CV_{nombre}.pdf",mime="application/pdf"):
        st.success(f"¡CV de {nombre} listo para descargar!")

if __name__ == "__main__":
    main()



 



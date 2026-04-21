from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import streamlit as st

def main():
    st.title("Generador de CV")

    #Datos Básicos
    st.header("Información Personal")
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Email")

    #Experiencia
    st.header("Experiencia Laboral")

    #Contadores para experiencia, educación, e idiomas
    if 'num_experiencia' not in st.session_state:
        st.session_state.num_experiencia = 1

    #Campos para experiencia
    for i in range(st.session_state.num_experiencia):
        with st.expander(f"Experiencia #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Puesto", key=f"puesto_{i}")
                st.text_input(f"Mes/Año Inicio", key=f"inicio_{i}")
            with col2:
                st.text_input(f"Empresa", key=f"empresa_{i}")
                st.text_input(f"Mes/Año Fin", key=f"fin_{i}")
                st.text_area(f"Tareas y logros", key=f"tareas_{i}")
            
    if st.button("➕ Agregar Experiencia"):
        st.session_state.num_experiencia += 1
        st.rerun()


    st.header("Educación")
    if 'num_educacion' not in st.session_state:
        st.session_state.num_educacion = 1

    #Campos para educación
    for i in range(st.session_state.num_educacion):
        with st.expander(f"Educación #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Titulo", key=f"titulo_{i}")
                st.text_input(f"Año", key=f"año_{i}")
            with col2:
                st.text_input(f"Institución", key=f"institucion_{i}")
   
    if st.button("➕ Agregar Educación"):
        st.session_state.num_educacion += 1
        st.rerun()

    #Campos para idiomas
    st.header("Idiomas")
    if 'num_idioma' not in st.session_state:
        st.session_state.num_idioma = 1
    
    #Campos para idioma
    for i in range(st.session_state.num_idioma):
        with st.expander(f"Idioma #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(f"Idioma", key=f"idioma_{i}")
                option = st.selectbox('Seleccione su nivel:',
                    ('Principiante', 'Intermedio', 'Avanzado', 'Nativo'), index=0,key=f"nivel_{i}")
   
    if st.button("➕ Agregar Idioma"):
        st.session_state.num_idioma += 1
        st.rerun()

    #Campos para habilidades
    habilidades = st.text_input("Habilidades (Separar con ,)")

    #Generación de PDF

    lista_experiencia = [{"Puesto": st.session_state[f"puesto_{i}"],"Empresa": st.session_state[f"empresa_{i}"],"Mes/Año Inicio": st.session_state[f"inicio_{i}"],"Fin": st.session_state[f"fin_{i}"],"Tareas y logros": st.session_state[f"tareas_{i}"]}
                            for i in range(st.session_state.num_experiencia)]
        
    lista_educacion = [{"Titulo": st.session_state[f"titulo_{i}"],"Año": st.session_state[f"año_{i}"],"Institución": st.session_state[f"institucion_{i}"],}
                           for i in range(st.session_state.num_educacion)]
        
    lista_idiomas = [{"Idioma": st.session_state[f"idioma_{i}"],"Nivel": st.session_state[f"nivel_{i}"]}
                         for i in range(st.session_state.num_idioma)]
        
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    titulo = Paragraph(f'{nombre}', styles['Title'])
    elementos = []
    elementos.append(Paragraph("EXPERIENCIA LABORAL", styles['Heading2']))
        
    for item in lista_experiencia:
        elementos.append(Paragraph(f"<b>{item['Puesto']}</b> en {item['Empresa']}", styles['Normal']))
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"{item['Tareas y logros']}", styles['Normal']))
        elementos.append(Spacer(1, 20))

    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph("EDUCACIÓN", styles['Heading2']))
    for item in lista_educacion:
        elementos.append(Paragraph(f"<b>{item['Titulo']}</b> - {item['Institución']}", styles['Normal']))
        elementos.append(Spacer(1, 10))   
            
    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph("IDIOMAS", styles['Heading2']))
    for item in lista_idiomas:
        elementos.append(Paragraph(f"• {item['Idioma']}: {item['Nivel']}", styles['Normal']))
            
    doc.build(elementos)
    pdf_final = buffer.getvalue()
    if st.download_button(label="📥 Descargar CV PDF",data=pdf_final,file_name=f"CV_{nombre}.pdf",mime="application/pdf"):
        st.success(f"¡CV de {nombre} listo para descargar!")

if __name__ == "__main__":
    main()



 



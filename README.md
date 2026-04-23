# CV-Builder

Aplicacion web hecha con Streamlit para crear un CV profesional y descargarlo en PDF en pocos pasos.

## Caracteristicas

- Formulario guiado para informacion personal, experiencia, educacion, idiomas, certificaciones y habilidades.
- Secciones dinamicas: puedes agregar multiples entradas en cada bloque.
- Editor enriquecido para tareas y logros en experiencia laboral.
- Generacion de CV en PDF lista para descargar.
- Interfaz simple y rapida para uso local.

## Tecnologias principales

- Python
- Streamlit
- ReportLab
- xhtml2pdf
- streamlit-quill

## Requisitos

- Python 3.10 o superior (recomendado)
- pip actualizado

## Instalacion

1. Clona este repositorio.
2. Entra a la carpeta del proyecto.
3. (Opcional, recomendado) Crea y activa un entorno virtual.
4. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion

Desde la raiz del proyecto, ejecuta:

```bash
streamlit run app.py
```

Luego abre en el navegador la URL que muestra Streamlit (normalmente http://localhost:8501).

## Como usar

1. Completa la seccion Informacion Personal.
2. Agrega tu Experiencia Laboral, incluyendo tareas y logros.
3. Completa Educacion, Idiomas, Certificaciones y Habilidades.
4. Usa los botones con simbolo + para agregar mas entradas donde lo necesites.
5. Haz clic en Descargar CV PDF para generar y bajar tu archivo.

## Estructura del proyecto

```text
CV-Builder/
	app.py              # Aplicacion principal Streamlit
	assets/
		screenshots/     # Capturas de pantalla del proyecto
		demo/            # GIF o video corto de demostracion
	requirements.txt    # Dependencias del proyecto
	README.md           # Documentacion
	LICENSE             # Licencia
```


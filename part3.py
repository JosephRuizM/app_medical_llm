# el cerebro de la ia
import os
import shutil
from tkinter import filedialog, messagebox
from google import genai
from part1 import guardar_ruta_archivo

# 🔑 Tu API Key real de Google AI Studio vinculada para siempre
API_KEY_GEMINI = "AIzaSyBSZAmKvGFGCvbjCOmnxFUCmaVivQOrvJg"


def simular_subida_nube(cedula_paciente):
    """Abre el explorador de Windows, copia el archivo a una carpeta en el Escritorio y lo registra en MySQL"""
    ruta_origen = filedialog.askopenfilename(
        title="📎 Seleccionar Documento Médico (PDF/Texto)",
        filetypes=[("Documentos Clínicos", "*.pdf *.txt *.docx")]
    )

    if not ruta_origen:
        return None

    try:
        # Detectamos la ruta del Escritorio de tu usuario de Windows automáticamente
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
        carpeta_nube_simulada = os.path.join(escritorio, "Nube_Hospital_Simulada")

        # Si la carpeta no existe en tu escritorio, Python la crea solita
        if not os.path.exists(carpeta_nube_simulada):
            os.makedirs(carpeta_nube_simulada)

        # Extraemos el nombre original del archivo y le anteponemos la cédula
        nombre_base = os.path.basename(ruta_origen)
        nombre_seguro = f"{cedula_paciente}_{nombre_base}"
        ruta_destino_final = os.path.join(carpeta_nube_simulada, nombre_seguro)

        # Copiamos el archivo físicamente a la carpeta simulada
        shutil.copy(ruta_origen, ruta_destino_final)

        # Guardamos el registro de la ruta en la base de datos
        guardar_ruta_archivo(cedula_paciente, nombre_base, ruta_destino_final)

        messagebox.showinfo("Simulación Cloud",
                            f"¡Archivo asociado con éxito!\nGuardado localmente en:\n{ruta_destino_final}")
        return nombre_base
    except Exception as e:
        messagebox.showerror("Error de Almacenamiento", f"No se pudo guardar el archivo localmente:\n{str(e)}")
        return None


def analizar_diagnostico_con_gemini(datos_texto_paciente):
    """Se conecta de forma gratuita a Gemini 1.5 Flash asegurando el registro de la clave"""
    if not API_KEY_GEMINI or API_KEY_GEMINI == "AIzaSy...":
        return "⚠️ CONFIGURACIÓN INCOMPLETA:\nPor favor, valida la API Key en part3.py."

    try:
        # 🔥 ESTA LÍNEA OBLIGA A WINDOWS A RECONOCER TU CLAVE AL 100% 🔥
        os.environ["GEMINI_API_KEY"] = API_KEY_GEMINI

        # Inicialización oficial con el SDK moderno genai (leerá la variable de entorno automáticamente)
        client = genai.Client()

        prompt = f"""
        Actúa como un sistema experto de soporte a la decisión clínica. Analiza la siguiente historia clínica extraída del paciente y genera un informe predictivo detallado sobre riesgos potenciales de salud.

        DATOS EXTRAÍDOS DEL PACIENTE DESDE MYSQL:
        {datos_texto_paciente}

        Estructura tu respuesta estrictamente con los siguientes títulos en mayúsculas:
        1. EVALUACIÓN GENERAL DE SIGNOS VITALES
        2. RIESGOS POTENCIALES DETECTADOS (Explica detalladamente las correlaciones médicas encontradas)
        3. RECOMENDACIONES PREVENTIVAS Y DE MONITOREO

        Termina el reporte incluyendo un descargo de responsabilidad indicando que esto es una simulación automatizada de soporte y debe ser validada obligatoriamente por un médico colegiado.
        """

        # Llamada gratuita al modelo optimizado
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        if response.text:
            return response.text
        else:
            return "⚠️ La IA procesó la solicitud pero no devolvió texto. Revisa la consistencia de los datos."

    except Exception as e:
        return f"❌ ERROR DE CONEXIÓN CON GEMINI AI:\n{str(e)}\n\nVerifica tu conexión a internet o el estado de tu clave."

import customtkinter as ctk
from tkinter import messagebox

# Importaciones desde tu archivo part1 suelto en la raíz
from part1 import (
    guardar_paciente_completo,
    buscar_paciente_en_db,
    eliminar_paciente,
    actualizar_paciente
)

# Conexión directa con tu nuevo módulo de simulación de IA y Nube
from part3 import simular_subida_nube, analizar_diagnostico_con_gemini


class AppUsuarios(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Control de Usuarios - Clínico")
        self.geometry("600x750")
        self.resizable(False, False)

        # --- REGISTRO DE VALIDADORES DEL TECLADO ---
        self.validador_entero = self.register(self.solo_numeros_enteros)
        self.validador_decimal = self.register(self.solo_numeros_decimales)

        # Contenedor dinámico de pantallas
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.mostrar_menu_principal()

    def limpiar_pantalla(self):
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    # --- PANTALLA DE INICIO (MENÚ PRINCIPAL) ---
    def mostrar_menu_principal(self):
        self.limpiar_pantalla()

        lbl_sistema = ctk.CTkLabel(
            self.contenedor_principal,
            text="Sistema de Salud\nIngreso de Pacientes",
            font=("Arial", 22, "bold"),
            text_color="#3a9ad9"
        )
        lbl_sistema.pack(pady=(40, 50))

        btn_nuevo = ctk.CTkButton(
            self.contenedor_principal,
            text="Ingresar Paciente Nuevo",
            width=300,
            height=45,
            font=("Arial", 14),
            command=self.disenar_pestana_registrar
        )
        btn_nuevo.pack(pady=12)

        btn_extraer = ctk.CTkButton(
            self.contenedor_principal,
            text="Extraer Datos de Paciente",
            width=300,
            height=45,
            font=("Arial", 14),
            command=self.disenar_pestana_consultar
        )
        btn_extraer.pack(pady=12)

        btn_eliminar = ctk.CTkButton(
            self.contenedor_principal,
            text="Eliminar Paciente",
            width=300,
            height=45,
            font=("Arial", 14),
            command=self.mostrar_pantalla_eliminar
        )
        btn_eliminar.pack(pady=12)

        btn_actualizar = ctk.CTkButton(
            self.contenedor_principal,
            text="Actualizar Estado de Paciente",
            width=300,
            height=45,
            font=("Arial", 14),
            command=self.mostrar_pantalla_actualizar
        )
        btn_actualizar.pack(pady=12)

        btn_salir = ctk.CTkButton(
            self.contenedor_principal,
            text="Salir del Sistema",
            fg_color="#d9534f",
            hover_color="#c9302c",
            width=300,
            height=45,
            font=("Arial", 14),
            command=self.quit
        )
        btn_salir.pack(pady=(60, 10))

    def solo_numeros_enteros(self, texto_futuro):
        if texto_futuro == "":
            return True
        return texto_futuro.isdigit() and len(texto_futuro) <= 15

    def solo_numeros_decimales(self, texto_futuro):
        if texto_futuro == "":
            return True
        try:
            if texto_futuro == ".":
                return True
            float(texto_futuro)
            return True
        except ValueError:
            return False

    def crear_titulo(self, contenedor, texto):
        label = ctk.CTkLabel(
            contenedor,
            text=texto,
            font=("Arial", 14, "bold"),
            text_color="#3a9ad9"
        )
        label.pack(pady=(15, 5))

    def crear_campo(
        self,
        contenedor,
        placeholder,
        empaquetar=True,
        width=420,
        es_numerico=False,
        es_decimal=False
    ):
        if empaquetar:
            lbl_campo = ctk.CTkLabel(
                contenedor,
                text=f"{placeholder}:",
                font=("Arial", 11, "bold"),
                anchor="w",
                width=width
            )
            lbl_campo.pack(pady=(4, 0))

            entrada = ctk.CTkEntry(
                contenedor,
                width=width,
                height=35
            )
        else:
            entrada = ctk.CTkEntry(
                contenedor,
                placeholder_text=placeholder,
                width=width,
                height=35
            )

        entrada.es_numerico = es_numerico
        entrada.es_decimal = es_decimal

        if es_numerico:
            entrada.configure(
                validate="key",
                validatecommand=(self.validador_entero, "%P")
            )

        elif es_decimal:
            entrada.configure(
                validate="key",
                validatecommand=(self.validador_decimal, "%P")
            )

        if empaquetar:
            entrada.pack(pady=(1, 5))

        return entrada

    # --- SECCIÓN 1: REGISTRAR PACIENTE NUEVO ---
    def disenar_pestana_registrar(self):
        self.limpiar_pantalla()

        scroll = ctk.CTkScrollableFrame(
            self.contenedor_principal,
            width=520,
            height=520
        )
        scroll.pack(padx=10, pady=10)

        btn_regresar = ctk.CTkButton(
            scroll,
            text="← Regresar al Menú Principal",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.mostrar_menu_principal
        )
        btn_regresar.pack(pady=(5, 15), anchor="w")

        # 1. Datos Personales
        self.crear_titulo(scroll, "1. Datos Personales")

        self.txt_cedula = self.crear_campo(
            scroll,
            "Número de Cédula",
            es_numerico=True
        )

        self.txt_nombre = self.crear_campo(scroll, "Nombre")
        self.txt_apellidos = self.crear_campo(scroll, "Apellidos")

        self.txt_telefono = self.crear_campo(
            scroll,
            "Teléfono",
            es_numerico=True
        )

        self.txt_correo = self.crear_campo(
            scroll,
            "Correo electrónico"
        )

        # 2. Historial Clínico
        self.crear_titulo(scroll, "2. Historial Clínico")

        self.txt_tipo_sangre = self.crear_campo(
            scroll,
            "Tipo de Sangre"
        )

        self.txt_alergias = self.crear_campo(scroll, "Alergias")

        self.txt_enfermedades = self.crear_campo(
            scroll,
            "Enfermedades Crónicas"
        )

        # 3. Contacto de Emergencia
        self.crear_titulo(scroll, "3. Contacto de Emergencia")

        self.txt_nom_contacto = self.crear_campo(
            scroll,
            "Nombre del Contacto"
        )

        self.txt_parentesco = self.crear_campo(
            scroll,
            "Parentesco"
        )

        self.txt_tel_emergencia = self.crear_campo(
            scroll,
            "Teléfono de Emergencia",
            es_numerico=True
        )

        # 4. Datos de la Consulta
        self.crear_titulo(scroll, "4. Datos de la Consulta")

        ctk.CTkLabel(
            scroll,
            text="Fecha de Consulta:",
            font=("Arial", 12)
        ).pack(pady=2)

        frame_fecha_con = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )
        frame_fecha_con.pack(pady=5)

        self.cb_mes_con = ctk.CTkComboBox(
            frame_fecha_con,
            values=[str(i) for i in range(1, 13)],
            width=85
        )
        self.cb_mes_con.set("Mes")
        self.cb_mes_con.pack(side="left", padx=5)

        self.txt_dia_con = self.crear_campo(
            frame_fecha_con,
            "Día",
            empaquetar=False,
            width=80,
            es_numerico=True
        )
        self.txt_dia_con.pack(side="left", padx=5)

        self.txt_anio_con = self.crear_campo(
            frame_fecha_con,
            "Año (AAAA)",
            empaquetar=False,
            width=110,
            es_numerico=True
        )
        self.txt_anio_con.pack(side="left", padx=5)

        self.txt_motivo = self.crear_campo(
            scroll,
            "Motivo de Consulta"
        )

        self.txt_diagnostico = self.crear_campo(
            scroll,
            "Diagnóstico"
        )

        self.txt_medico_id = self.crear_campo(
            scroll,
            "ID del Médico (Número)",
            es_numerico=True
        )

        # 5. Signos Vitales
        self.crear_titulo(scroll, "5. Signos Vitales")

        ctk.CTkLabel(
            scroll,
            text="Fecha Registro Signos:",
            font=("Arial", 12)
        ).pack(pady=2)

        frame_fecha_sig = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )
        frame_fecha_sig.pack(pady=5)

        self.cb_mes_sig = ctk.CTkComboBox(
            frame_fecha_sig,
            values=[str(i) for i in range(1, 13)],
            width=85
        )
        self.cb_mes_sig.set("Mes")
        self.cb_mes_sig.pack(side="left", padx=5)

        self.txt_dia_sig = self.crear_campo(
            frame_fecha_sig,
            "Día",
            empaquetar=False,
            width=80,
            es_numerico=True
        )
        self.txt_dia_sig.pack(side="left", padx=5)

        self.txt_anio_sig = self.crear_campo(
            frame_fecha_sig,
            "Año (AAAA)",
            empaquetar=False,
            width=110,
            es_numerico=True
        )
        self.txt_anio_sig.pack(side="left", padx=5)

        self.txt_presion = self.crear_campo(
            scroll,
            "Presión arterial (ej: 120/80)"
        )

        self.txt_frecuencia = self.crear_campo(
            scroll,
            "Frecuencia cardíaca (lpm)",
            es_numerico=True
        )

        self.txt_temperatura = self.crear_campo(
            scroll,
            "Temperatura (°C)",
            es_decimal=True
        )

        btn_guardar = ctk.CTkButton(
            scroll,
            text="Guardar Formulario Completo",
            fg_color="#2eb85c",
            hover_color="#239249",
            height=40,
            font=("Arial", 13, "bold"),
            command=self.click_guardar
        )
        btn_guardar.pack(pady=30)

    # --- LÓGICA DE VALIDACIÓN DE FECHAS (ALGORITMO BISIESTO) ---
    def validar_y_formatear_fecha(
        self,
        combo_mes,
        entrada_dia,
        entrada_anio,
        nombre_campo
    ):
        mes_txt = combo_mes.get()
        dia_txt = entrada_dia.get()
        anio_txt = entrada_anio.get()

        if mes_txt == "Mes" or not dia_txt or not anio_txt:
            messagebox.showerror(
                "Error de Fecha",
                f"Debe completar el Mes, Día y Año en el campo {nombre_campo}."
            )
            return None

        mes, dia, anio = int(mes_txt), int(dia_txt), int(anio_txt)

        if anio < 1900 or anio > 2100:
            messagebox.showerror(
                "Error de Rango",
                f"El Año en {nombre_campo} debe estar entre 1900 y 2100."
            )
            return None

        de_31_dias = [1, 3, 5, 7, 8, 10, 12]

        if mes in de_31_dias:
            limite_dias = 31

        elif mes == 2:
            es_bisiesto = (
                (anio % 4 == 0 and anio % 100 != 0)
                or
                (anio % 400 == 0)
            )

            limite_dias = 29 if es_bisiesto else 28

        else:
            limite_dias = 30

        if dia < 1 or dia > limite_dias:
            messagebox.showerror(
                "Error de Día",
                f"Día inválido para el mes y año seleccionados en {nombre_campo}."
            )
            return None

        return f"{anio}-{mes:02d}-{dia:02d}"

    def click_guardar(self):
        cedula_id = self.txt_cedula.get().strip()

        fecha_consulta = self.validar_y_formatear_fecha(
            self.cb_mes_con,
            self.txt_dia_con,
            self.txt_anio_con,
            "Datos de la Consulta"
        )

        if not fecha_consulta:
            return

        fecha_signos = self.validar_y_formatear_fecha(
            self.cb_mes_sig,
            self.txt_dia_sig,
            self.txt_anio_sig,
            "Signos Vitales"
        )

        if not fecha_signos:
            return

        p_datos = (
            self.txt_nombre.get().strip(),
            self.txt_apellidos.get().strip(),
            self.txt_telefono.get().strip(),
            self.txt_correo.get().strip()
        )

        h_datos = (
            self.txt_tipo_sangre.get().strip(),
            self.txt_alergias.get().strip(),
            self.txt_enfermedades.get().strip()
        )

        c_datos = (
            self.txt_nom_contacto.get().strip(),
            self.txt_parentesco.get().strip(),
            self.txt_tel_emergencia.get().strip()
        )

        m_datos = (
            fecha_consulta,
            self.txt_motivo.get().strip(),
            self.txt_diagnostico.get().strip(),
            self.txt_medico_id.get().strip()
        )

        s_datos = (
            fecha_signos,
            self.txt_presion.get().strip(),
            self.txt_frecuencia.get().strip(),
            self.txt_temperatura.get().strip()
        )

        if (
            not cedula_id
            or not self.txt_nombre.get().strip()
            or not self.txt_apellidos.get().strip()
        ):
            messagebox.showwarning(
                "Campos Obligatorios",
                "La Cédula, el Nombre y los Apellidos son estrictamente requeridos."
            )
            return

        try:
            guardar_paciente_completo(
                cedula_id,
                p_datos,
                h_datos,
                c_datos,
                m_datos,
                s_datos
            )

            messagebox.showinfo(
                "Operación Exitosa",
                f"Todos los datos clínicos se guardaron correctamente bajo la Cédula: {cedula_id}"
            )

            self.mostrar_menu_principal()

        except Exception as e:
            messagebox.showerror(
                "Error de base de datos",
                f"Hubo un fallo al insertar los registros:\n{str(e)}"
            )

    # --- SECCIÓN 2: EXTRAER DATOS (BUSCAR / CONSULTAR CON IA) ---
    def disenar_pestana_consultar(self):
        self.limpiar_pantalla()

        btn_regresar = ctk.CTkButton(
            self.contenedor_principal,
            text="← Regresar al Menú Principal",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.mostrar_menu_principal
        )
        btn_regresar.pack(pady=5, anchor="w")

        self.crear_titulo(
            self.contenedor_principal,
            "Búsqueda Avanzada de Pacientes"
        )

        self.txt_buscar_id = self.crear_campo(
            self.contenedor_principal,
            "Cédula del Paciente a Buscar",
            es_numerico=True
        )

        lbl_combo = ctk.CTkLabel(
            self.contenedor_principal,
            text="Seleccione tipo de datos a extraer:",
            font=("Arial", 11, "bold"),
            anchor="w",
            width=420
        )
        lbl_combo.pack(pady=(4, 0))

        self.cb_opciones = ctk.CTkComboBox(
            self.contenedor_principal,
            values=[
                "1. Reporte Completo",
                "2. Solo Nombre",
                "3. Solo Correo"
            ],
            width=420
        )

        self.cb_opciones.set("1. Reporte Completo")
        self.cb_opciones.pack(pady=(1, 10))

        # Panel de acciones horizontales
        frame_botones = ctk.CTkFrame(
            self.contenedor_principal,
            fg_color="transparent"
        )
        frame_botones.pack(pady=5)

        btn_buscar = ctk.CTkButton(
            frame_botones,
            text="Buscar Registros",
            fg_color="#3a9ad9",
            hover_color="#2b76a6",
            command=self.click_buscar
        )
        btn_buscar.pack(side="left", padx=5)

        btn_adjuntar = ctk.CTkButton(
            frame_botones,
            text="📎 Adjuntar Historial",
            fg_color="#6c757d",
            hover_color="#495057",
            command=self.click_adjuntar_archivo
        )
        btn_adjuntar.pack(side="left", padx=5)

        self.btn_ia = ctk.CTkButton(
            self.contenedor_principal,
            text="🤖 Analizar Datos Extraídos (Gemini IA)",
            fg_color="#8a4af3",
            hover_color="#7032d6",
            state="disabled",
            command=self.click_analizar_ia
        )
        self.btn_ia.pack(pady=5)

        self.txt_resultados = ctk.CTkTextbox(
            self.contenedor_principal,
            width=500,
            height=310,
            font=("Courier New", 12)
        )
        self.txt_resultados.pack(pady=10)

    def click_adjuntar_archivo(self):
        cedula = self.txt_buscar_id.get().strip()

        if not cedula:
            messagebox.showwarning(
                "Atención",
                "Por favor, digite primero la cédula del paciente."
            )
            return

        simular_subida_nube(cedula)

    def click_buscar(self):
        id_buscado = self.txt_buscar_id.get().strip()
        opcion_datos = self.cb_opciones.get()

        if not id_buscado:
            messagebox.showwarning(
                "Atención",
                "Por favor, ingrese una Cédula válida."
            )
            return

        self.txt_resultados.delete("1.0", "end")

        resultados = buscar_paciente_en_db(
            id_buscado,
            opcion_datos
        )

        if not resultados:
            self.txt_resultados.insert(
                "end",
                f"No se encontraron registros clínicos para la Cédula: {id_buscado}."
            )

            self.btn_ia.configure(state="disabled")
            return

        self.txt_resultados.insert(
            "end",
            f"=== HISTORIAL ENCONTRADO (CÉDULA: {id_buscado}) ===\n\n"
        )

        if "1." in opcion_datos:
            campos = [
                "Nombre",
                "Apellidos",
                "Teléfono",
                "Correo",
                "Tipo de Sangre",
                "Alergias",
                "Contacto Emergencia",
                "Diagnóstico",
                "Temperatura (°C)"
            ]

            for campo, valor in zip(campos, resultados):
                self.txt_resultados.insert(
                    "end",
                    f"➤ {campo.upper()}: {valor}\n"
                )

            self.btn_ia.configure(state="normal")

        elif "2." in opcion_datos:
            self.txt_resultados.insert(
                "end",
                f"➤ NOMBRE COMPLETO: {resultados}\n"
            )

            self.btn_ia.configure(state="disabled")

        elif "3." in opcion_datos:
            self.txt_resultados.insert(
                "end",
                f"➤ CORREO ELECTRÓNICO: {resultados}\n"
            )

            self.btn_ia.configure(state="disabled")

    def click_analizar_ia(self):
        texto_pantalla = self.txt_resultados.get(
            "1.0",
            "end"
        ).strip()

        self.txt_resultados.delete("1.0", "end")

        self.txt_resultados.insert(
            "end",
            "🤖 Conectando con Gemini... Procesando historial clínico. Espere un momento...\n\n"
        )

        self.update_idletasks()

        reporte_ia = analizar_diagnostico_con_gemini(
            texto_pantalla
        )

        self.txt_resultados.delete("1.0", "end")
        self.txt_resultados.insert("end", reporte_ia)

    # --- SECCIÓN 3: ELIMINAR PACIENTE ---
    def mostrar_pantalla_eliminar(self):
        self.limpiar_pantalla()

        btn_regresar = ctk.CTkButton(
            self.contenedor_principal,
            text="← Regresar al Menú Principal",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.mostrar_menu_principal
        )
        btn_regresar.pack(pady=5, anchor="w")

        self.crear_titulo(
            self.contenedor_principal,
            "Eliminación de Historias Clínicas"
        )

        self.txt_eliminar_id = self.crear_campo(
            self.contenedor_principal,
            "Cédula del Paciente a Eliminar",
            es_numerico=True
        )

        btn_confirmar = ctk.CTkButton(
            self.contenedor_principal,
            text="Eliminar Permanentemente",
            fg_color="#d9534f",
            hover_color="#c9302c",
            height=40,
            command=self.click_eliminar
        )
        btn_confirmar.pack(pady=20)

    def click_eliminar(self):
        id_del = self.txt_eliminar_id.get().strip()

        if not id_del:
            messagebox.showwarning(
                "Atención",
                "Debe especificar una Cédula válida."
            )
            return

        if messagebox.askyesno(
            "Confirmar acción",
            f"¿Está seguro de que desea eliminar el registro vinculado a la Cédula #{id_del}?\nEsta acción borrará todo el historial clínico."
        ):
            try:
                if eliminar_paciente(id_del):
                    messagebox.showinfo(
                        "Éxito",
                        "El paciente y todo su historial han sido eliminados de la base de datos."
                    )

                    self.mostrar_menu_principal()

                else:
                    messagebox.showerror(
                        "Error de búsqueda",
                        "La Cédula ingresada no coincide con ningún registro activo."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo completar la operación:\n{str(e)}"
                )

    # --- SECCIÓN 4: ACTUALIZAR ESTADO ---
    def mostrar_pantalla_actualizar(self):
        self.limpiar_pantalla()

        btn_regresar = ctk.CTkButton(
            self.contenedor_principal,
            text="← Regresar al Menú Principal",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.mostrar_menu_principal
        )
        btn_regresar.pack(pady=5, anchor="w")

        self.crear_titulo(
            self.contenedor_principal,
            "Modificar Información de Pacientes"
        )

        self.txt_act_id = self.crear_campo(
            self.contenedor_principal,
            "Cédula del Paciente a Actualizar",
            es_numerico=True
        )

        lbl_col = ctk.CTkLabel(
            self.contenedor_principal,
            text="Seleccione el campo a actualizar:",
            font=("Arial", 11, "bold"),
            anchor="w",
            width=420
        )
        lbl_col.pack(pady=(4, 0))

        self.cb_columnas = ctk.CTkComboBox(
            self.contenedor_principal,
            values=["nombre", "apellidos", "telefono", "correo"],
            width=420
        )

        self.cb_columnas.set("nombre")
        self.cb_columnas.pack(pady=(1, 10))

        self.txt_nuevo_valor = self.crear_campo(
            self.contenedor_principal,
            "Nuevo valor / Actualización"
        )

        btn_update = ctk.CTkButton(
            self.contenedor_principal,
            text="Guardar Cambios",
            fg_color="#2eb85c",
            hover_color="#239249",
            height=40,
            command=self.click_actualizar
        )
        btn_update.pack(pady=20)

    def click_actualizar(self):
        id_act = self.txt_act_id.get().strip()
        columna = self.cb_columnas.get()
        valor = self.txt_nuevo_valor.get().strip()

        if not id_act or not valor:
            messagebox.showwarning(
                "Atención",
                "Todos los campos son obligatorios para realizar la actualización."
            )
            return

        try:
            if actualizar_paciente(id_act, columna, valor):
                messagebox.showinfo(
                    "Éxito",
                    "La información del paciente fue modificada correctamente."
                )

                self.mostrar_menu_principal()

            else:
                messagebox.showerror(
                    "Error de actualización",
                    "No se encontró el número de Cédula o el campo no es modificable."
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo completar la operación:\n{str(e)}"
            )


if __name__ == "__main__":
    app = AppUsuarios()
    app.mainloop()
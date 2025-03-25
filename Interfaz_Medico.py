from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from mysql.connector.types import ParamsSequenceOrDictType
from DatabaseManager import DatabaseManager
from Interfaz_Reagendar import WindowReagendar

class WindowMedico(QMainWindow):

    def __init__(self, user_data):
        super().__init__()

        # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.setWindowIcon(QIcon('C:\Consultorio\doctor.ico'))  # Icono de la ventana de la aplicacion

        self.user_data = user_data
        self.id_usuario = user_data[5] # ID del doctor (usuario)
        self.ID_CitaSeleccionada = 0
        self.NombreApellidoPaciente = None

        #self.resize(1388, 775)
        self.setFixedSize(1388, 775)
        self.setWindowTitle('Consultorio Medico || Medico Especialista')
        self.setCentralWidget(QWidget(self))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.create_widgets()

        self.LabelMedico() # Mostrar el nombre del medico en la ventana
        self.CitasMedicasActivas()

    def create_widgets(self):
        self.GpCitas = QGroupBox(self)
        self.GpCitas.setGeometry(680, 72, 664, 616)
        self.GpCitas.setFont(QFont('Segoe UI', 9))
        self.GpCitas.setTitle('Resgistro de citas')
        self.GralData = QFrame(self)
        self.GralData.setGeometry(16, 16, 640, 208)
        self.GralData.setFont(QFont('Segoe UI', 9))
        self.GpDiagnostico = QGroupBox(self)
        self.GpDiagnostico.setGeometry(16, 232, 641, 528)
        self.GpDiagnostico.setFont(QFont('Segoe UI', 9))
        self.GpDiagnostico.setTitle('Diagnostico y Tratamiento')
        self.lblConsulEsp = QLabel(self.GralData)
        self.lblConsulEsp.setGeometry(112, 8, 392, 24)
        self.lblConsulEsp.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        # LEtras doradas
        self.lblConsulEsp.setStyleSheet("color: #FFD700;")
        self.lblConsulEsp.setText('Consultorio Medico Especializado')
        self.lMedico = QLabel(self.GralData)
        self.lMedico.setGeometry(48, 64, 88, 24)
        self.lMedico.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.lMedico.setText('Medico :')
        self.lEspecialidad = QLabel(self.GralData)
        self.lEspecialidad.setGeometry(8, 104, 129, 29)
        self.lEspecialidad.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.lEspecialidad.setText('Especialidad :')
        self.lPaciente = QLabel(self.GralData)
        self.lPaciente.setGeometry(16, 160, 96, 29)
        self.lPaciente.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.lPaciente.setText('Paciente :')
        self.lHistorialClinico = QLabel(self)
        self.lHistorialClinico.setGeometry(928, 24, 208, 34)
        self.lHistorialClinico.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lHistorialClinico.setText('Historial Clinico')
        self.lDiagnosticodelpaciente = QLabel(self.GpDiagnostico)
        self.lDiagnosticodelpaciente.setGeometry(16, 48, 240, 24)
        self.lDiagnosticodelpaciente.setFont(QFont('Consolas', 12, QFont.Weight.Bold))
        self.lDiagnosticodelpaciente.setText('Diagnostico del paciente')
        self.lTratamiento = QLabel(self.GpDiagnostico)
        self.lTratamiento.setGeometry(16, 168, 240, 24)
        self.lTratamiento.setFont(QFont('Consolas', 12, QFont.Weight.Bold))
        self.lTratamiento.setText('Tratamiento')
        self.lObservacionesycomentarios = QLabel(self.GpDiagnostico)
        self.lObservacionesycomentarios.setGeometry(16, 296, 252, 24)
        self.lObservacionesycomentarios.setFont(QFont('Consolas', 12, QFont.Weight.Bold))
        self.lObservacionesycomentarios.setText('Observaciones y comentarios')
        
        # Lineas de texto para el paciente
        self.lineEdit1 = QLineEdit(self.GralData)
        self.lineEdit1.setGeometry(120, 160, 345, 33)
        self.lineEdit1.setFont(QFont('Segoe UI', 9))

        # Tablas de diagnostico y Entrada de texto
        self.PlainDiagnostico = QPlainTextEdit(self.GpDiagnostico)
        self.PlainDiagnostico.setGeometry(16, 72, 608, 80)
        self.PlainDiagnostico.setFont(QFont('Segoe UI', 9))

        self.PlainTratamiento = QPlainTextEdit(self.GpDiagnostico)
        self.PlainTratamiento.setGeometry(16, 192, 608, 80)
        self.PlainTratamiento.setFont(QFont('Segoe UI', 9))

        self.PlainObservaciones = QPlainTextEdit(self.GpDiagnostico)
        self.PlainObservaciones.setGeometry(16, 320, 608, 80)
        self.PlainObservaciones.setFont(QFont('Segoe UI', 9))

        self.TableCitasActivas = QTableView(self.GpCitas)
        self.TableCitasActivas.setGeometry(16, 32, 633, 569)
        self.TableCitasActivas.setFont(QFont('Segoe UI', 9))
        self.TableCitasActivas.setModel(QStandardItemModel())
        self.TableCitasActivas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.TableCitasActivas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.TableCitasActivas.selectionModel().selectionChanged.connect(self.seleccionar_paciente)
        self.TableCitasActivas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.TableCitasActivas.setSortingEnabled(True)
        self.TableCitasActivas.setAlternatingRowColors(True)
        self.TableCitasActivas.clicked.connect(self.cargar_detalles_diagnostico)  # Actualizar detalles al seleccionar una cita
        
        # Botones de accion de la aplicacion
        self.BtnDiagnostico = QToolButton(self.GpDiagnostico)
        self.BtnDiagnostico.setGeometry(16, 456, 136, 48)
        self.BtnDiagnostico.setStyleSheet("background-color: #FF126905; color: white;")
        self.BtnDiagnostico.setFont(QFont('Segoe UI', 9))
        self.BtnDiagnostico.setText('Registrar Diagnostico')
        self.BtnDiagnostico.clicked.connect(self.BtnDiagnostico_clicked)

        self.BtnCancelarCita = QToolButton(self.GpDiagnostico)
        self.BtnCancelarCita.setGeometry(168, 456, 136, 48)
        self.BtnCancelarCita.setStyleSheet("background-color: #FF690E10; color: white;")
        self.BtnCancelarCita.setFont(QFont('Segoe UI', 9))
        self.BtnCancelarCita.setText('Cancelar Cita')
        self.BtnCancelarCita.clicked.connect(self.BtnCancelarCita_clicked)

        self.BtnReprogramar = QToolButton(self.GpDiagnostico)
        self.BtnReprogramar.setGeometry(312, 456, 136, 48)
        self.BtnReprogramar.setStyleSheet("background-color: #FF083869; color: white;")
        self.BtnReprogramar.setFont(QFont('Segoe UI', 9))
        self.BtnReprogramar.setText('Reprogramar Cita')
        self.BtnReprogramar.clicked.connect(self.BtnReprogramar_clicked)

        self.BtnCerrarSesion = QToolButton(self)
        self.BtnCerrarSesion.setGeometry(1168, 704, 160, 48)
        self.BtnCerrarSesion.setStyleSheet("background-color: #FF460769; color: white;")
        self.BtnCerrarSesion.setFont(QFont('Segoe UI', 9))
        self.BtnCerrarSesion.setText('Cerrar Sesion')
        self.BtnCerrarSesion.clicked.connect(self.BtnCerrarSesion_clicked)

        self.BtnBuscarPAciente = QToolButton(self.GralData)
        self.BtnBuscarPAciente.setGeometry(480, 160, 120, 32) # Boton color Azul
        self.BtnBuscarPAciente.setStyleSheet("background-color: #007bff; color: white;")
        self.BtnBuscarPAciente.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.BtnBuscarPAciente.setText('Buscar Paciente')
        self.BtnBuscarPAciente.clicked.connect(self.BtnBuscarPAciente_clicked)

        # self.BtnDetallesDiag = QToolButton(self.GpDiagnostico)
        # self.BtnDetallesDiag.setGeometry(456, 456, 160, 48)
        # self.BtnDetallesDiag.setStyleSheet("background-color: #FF17695E; color: white;")
        # self.BtnDetallesDiag.setFont(QFont('Segoe UI', 9))
        # self.BtnDetallesDiag.setText('Detalles del Diagnostico')
        # self.BtnDetallesDiag.clicked.connect(self.BtnDetallesDiag_clicked)

        self.btnClearSel = QToolButton(self.GralData)
        self.btnClearSel.setGeometry(480, 112, 120, 32)
        self.btnClearSel.setStyleSheet("background-color: #FF460769; color: white;")
        self.btnClearSel.setFont(QFont('Segoe UI', 9))
        self.btnClearSel.setText('Clear Selection')
        self.btnClearSel.clicked.connect(self.btnClearSel_clicked)

        # Labels de cambio segun el inicio de sesion
        self.LblEspecialidadDoc = QLabel(self.GralData)
        self.LblEspecialidadDoc.setGeometry(144, 104, 304, 29)
        self.LblEspecialidadDoc.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.LblEspecialidadDoc.setText('--------------------') # Especialidad del medico
        self.LblMedicoEsp = QLabel(self.GralData)
        self.LblMedicoEsp.setGeometry(144, 64, 304, 29)
        self.LblMedicoEsp.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.LblMedicoEsp.setText('--------------------') # Nombre del medico
        
        pass

    def BtnCerrarSesion_clicked(self, checked):
        self.close()
        self.mostrar_ventana_login() # Mostrar la ventana de inicio de sesión

    def BtnDiagnostico_clicked(self, checked):
        # Obtener el ID de la cita seleccionada
        selectIndex = self.TableCitasActivas.selectedIndexes()
        if len(selectIndex) == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita para registrar el diagnóstico.")
            return

        # Obtener el ID de la cita seleccionada
        self.ObtenerCitaNombre()
        if self.ID_CitaSeleccionada == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita válida.")
            return

        # Obtener el diagnóstico, tratamiento y observaciones de los campos de texto
        diagnostico = self.PlainDiagnostico.toPlainText()
        tratamiento = self.PlainTratamiento.toPlainText()
        observaciones = self.PlainObservaciones.toPlainText()

        # Validar que se haya ingresado un diagnóstico
        if not diagnostico.strip():
            QMessageBox.warning(self, "Error", "El campo de diagnóstico no puede estar vacío.")
            return

        # Llamar al stored procedure para guardar el diagnóstico y completar la cita
        try:
            success, message = self.db_manager.guardar_diagnostico_y_completar_cita(
                self.ID_CitaSeleccionada, diagnostico, tratamiento, observaciones
            )
            if success:
                QMessageBox.information(self, "Éxito", "Diagnóstico registrado y cita completada con éxito.")
                # Actualizar la tabla de citas activas
                self.CitasMedicasActivas()
                self.LimpiarCampos()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar el diagnóstico: {message}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error inesperado: {str(e)}")

    def BtnCancelarCita_clicked(self, checked):
        # Cancelar la cita seleccionada
        selectIndex = self.TableCitasActivas.selectedIndexes()
        if len(selectIndex) == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita para cancelar.")
            return
        self.ObtenerCitaNombre()
        if self.ID_CitaSeleccionada == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita para cancelar.")
            return
        # Preguntar al usuario si está seguro de cancelar la cita
        respuesta = QMessageBox.question(self, "Cancelar cita", "¿Está seguro de cancelar la cita seleccionada?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if respuesta == QMessageBox.StandardButton.Yes:
            success, message = self.db_manager.cancelar_cita(self.ID_CitaSeleccionada)
            if success:
                QMessageBox.information(self, "Éxito", "Cita cancelada con éxito.")
                # Actualizar la tabla de citas activas
                self.CitasMedicasActivas()
                self.LimpiarCampos()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo cancelar la cita: {message}")
                
        pass

    def BtnReprogramar_clicked(self, checked):
        selectIndex = self.TableCitasActivas.selectedIndexes()
        if len(selectIndex) == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita para reprogramar.")
            return
        self.ObtenerCitaNombre()
        if self.ID_CitaSeleccionada == 0:
            QMessageBox.warning(self, "Error", "Seleccione una cita para reprogramar.")
            return
        self.AbrirReagendar()
        
        pass

    def BtnBuscarPAciente_clicked(self, checked):
        # Filtrar la tabla por nombre o apellido del paciente
        texto_busqueda = self.lineEdit1.text().strip()

        if texto_busqueda == "":  # Si el campo esta vacio, devolver la tabla a su estado original
            self.CitasMedicasActivas()
        else:
            IDMEDICO = self.id_usuario
            success, data = self.db_manager.cargar_citas_medico(IDMEDICO)
            if not success:
                QMessageBox.warning(self, "Error", data)
                return
            
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels([
                "ID Cita", "Nombre Paciente", "Apellido Paciente", 
                "Fecha y Hora", "Estado"
            ])

            # Filtrar las citas que contengan el texto de búsqueda en el nombre o apellido del paciente
            for cita in data:
                nombre_paciente = cita[1].lower()  # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas
                apellido_paciente = cita[2].lower()  # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas
                if texto_busqueda.lower() in nombre_paciente or texto_busqueda.lower() in apellido_paciente:
                    row = [
                        QStandardItem(str(cita[0])),  # ID Cita
                        QStandardItem(cita[1]),      # Nombre Paciente
                        QStandardItem(cita[2]),      # Apellido Paciente
                        QStandardItem(str(cita[3])),  # Fecha y Hora
                        QStandardItem(cita[4])       # Estado
                    ]
                    model.appendRow(row)

            # Establecer el modelo de la tabla con los datos filtrados
            self.TableCitasActivas.setModel(model)

            # Ajustar el tamaño de las columnas
            self.TableCitasActivas.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.TableCitasActivas.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.TableCitasActivas.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.TableCitasActivas.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            self.TableCitasActivas.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.TableCitasActivas.setColumnWidth(0, 80)
            self.TableCitasActivas.setColumnWidth(1, 150)
            self.TableCitasActivas.setColumnWidth(2, 150)
            self.TableCitasActivas.setColumnWidth(3, 150)
            self.TableCitasActivas.setColumnWidth(4, 150)

            # Establecer colores para las filas según el estado de la cita
            for i in range(model.rowCount()):
                if model.item(i, 4).text() == "cancelada":
                    model.item(i, 0).setBackground(QColor(255, 0, 0, 50))  # Rojo
                    model.item(i, 1).setBackground(QColor(255, 0, 0, 50))
                    model.item(i, 2).setBackground(QColor(255, 0, 0, 50))
                    model.item(i, 3).setBackground(QColor(255, 0, 0, 50))
                    model.item(i, 4).setBackground(QColor(255, 0, 0, 50))
                elif model.item(i, 4).text() == "completada":
                    model.item(i, 0).setBackground(QColor(0, 255, 0, 50))  # Verde
                    model.item(i, 1).setBackground(QColor(0, 255, 0, 50))
                    model.item(i, 2).setBackground(QColor(0, 255, 0, 50))
                    model.item(i, 3).setBackground(QColor(0, 255, 0, 50))
                    model.item(i, 4).setBackground(QColor(0, 255, 0, 50))
                elif model.item(i, 4).text() == "programada":
                    model.item(i, 0).setBackground(QColor(255, 255, 0, 50))  # Amarillo
                    model.item(i, 1).setBackground(QColor(255, 255, 0, 50))
                    model.item(i, 2).setBackground(QColor(255, 255, 0, 50))
                    model.item(i, 3).setBackground(QColor(255, 255, 0, 50))
                    model.item(i, 4).setBackground(QColor(255, 255, 0, 50))

    # def BtnDetallesDiag_clicked(self, checked):
    #     # ToDo insert source code here
    #     pass
    
    def btnClearSel_clicked(self, checked):
        self.LimpiarCampos()
        pass


    # Funciones de la ventana de inicio de sesión
    def mostrar_ventana_login(self):
        """Muestra la ventana de inicio de sesión."""
        from Main import LogInWindow  # Importar la ventana de inicio de sesión
        self.ventana_login = LogInWindow()
        self.ventana_login.show()

    def LabelMedico(self):
        success, data = self.db_manager.obtener_medicos()
        if not success:
            QMessageBox.warning(self, "Error", data)
            return
        for medico in data:
            if medico[0] == self.id_usuario:
                self.LblMedicoEsp.setText(medico[1] + " " + medico[2])
                self.LblEspecialidadDoc.setText(medico[3])
                break
        pass

    def CitasMedicasActivas(self):
        IDMEDICO = self.id_usuario
        success, data = self.db_manager.cargar_citas_medico(IDMEDICO)
        if not success:
            QMessageBox.warning(self, "Error", data)
            return
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "ID Cita", "Nombre Paciente", "Apellido Paciente", 
            "Fecha y Hora", "Estado"
        ])
        for cita in data:
            row = [
                QStandardItem(str(cita[0])),  # ID Cita
                QStandardItem(cita[1]),      # Nombre Paciente
                QStandardItem(cita[2]),      # Apellido Paciente
                QStandardItem(str(cita[3])),  # Fecha y Hora
                QStandardItem(cita[4])       # Estado
            ]
            model.appendRow(row)
        self.TableCitasActivas.setModel(model)
        # Ajustar el tamaño de las columnas setGeometry(16, 32, 633, 569)
        self.TableCitasActivas.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.TableCitasActivas.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.TableCitasActivas.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.TableCitasActivas.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.TableCitasActivas.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.TableCitasActivas.setColumnWidth(0, 80)
        self.TableCitasActivas.setColumnWidth(1, 150)
        self.TableCitasActivas.setColumnWidth(2, 150)
        self.TableCitasActivas.setColumnWidth(3, 150)
        self.TableCitasActivas.setColumnWidth(4, 150)
        # Si el estado de la cita es "Cancelada" o "Atendida", cambiar el color de la fila
        for i in range(model.rowCount()):
            if model.item(i, 4).text() == "cancelada":
                model.item(i, 0).setBackground(QColor(255, 0, 0, 50))  # Rojo
                model.item(i, 1).setBackground(QColor(255, 0, 0, 50))
                model.item(i, 2).setBackground(QColor(255, 0, 0, 50))
                model.item(i, 3).setBackground(QColor(255, 0, 0, 50))
                model.item(i, 4).setBackground(QColor(255, 0, 0, 50))
            elif model.item(i, 4).text() == "completada":
                model.item(i, 0).setBackground(QColor(0, 255, 0, 50))
                model.item(i, 1).setBackground(QColor(0, 255, 0, 50))
                model.item(i, 2).setBackground(QColor(0, 255, 0, 50))
                model.item(i, 3).setBackground(QColor(0, 255, 0, 50))
                model.item(i, 4).setBackground(QColor(0, 255, 0, 50))
            elif model.item(i, 4).text() == "programada":
                model.item(i, 0).setBackground(QColor(255, 255, 0, 50))
                model.item(i, 1).setBackground(QColor(255, 255, 0, 50))
                model.item(i, 2).setBackground(QColor(255, 255, 0, 50))
                model.item(i, 3).setBackground(QColor(255, 255, 0, 50))
                model.item(i, 4).setBackground(QColor(255, 255, 0, 50))
        
        pass

    def ObtenerCitaNombre(self):
        # Obtener el nombre del paciente de la cita seleccionada en la tabla
        index = self.TableCitasActivas.currentIndex()
        if index.isValid():
            self.ID_CitaSeleccionada = self.TableCitasActivas.model().index(index.row(), 0).data()
            self.NombreApellidoPaciente = self.TableCitasActivas.model().index(index.row(), 1).data() + " " + self.TableCitasActivas.model().index(index.row(), 2).data()
            self.lineEdit1.setText(self.NombreApellidoPaciente)
        else:
            self.ID_CitaSeleccionada = 0
            self.NombreApellidoPaciente = None

    def AbrirReagendar(self):
        # Abrir la ventana de reagendar cita
        self.ventana_reagendar = WindowReagendar(self.ID_CitaSeleccionada, self.NombreApellidoPaciente)
        # Conectar la señal de la ventana de reagendar a un método para actualizar la tabla
        self.ventana_reagendar.cita_reagendada.connect(self.SenalRecibida)
        self.ventana_reagendar.show()
        pass

    def SenalRecibida(self):
        # Actualizar la tabla de citas activas
        #limpiar la tabla
        self.db_manager.connect()
        self.CitasMedicasActivas()
        self.db_manager.disconnect()
        print("Señal recibida")
        pass

    def seleccionar_paciente(self, selected, deselected):
        """Obtiene el nombre del paciente de la fila seleccionada y lo muestra en lineEdit1."""
        print("Seleccion realziada")
        indexes = self.TableCitasActivas.currentIndex()
        if indexes:
            row = indexes[0].row()
            model = self.TableCitasActivas.model()
            nombre_paciente = model.item(row, 1).text()  # Columna 1: Nombre del paciente
            apellido_paciente = model.item(row, 2).text()  # Columna 2: Apellido del paciente
            self.lineEdit1.setText(f"{nombre_paciente} {apellido_paciente}")
        else:
            self.lineEdit1.clear()
        pass

    def LimpiarCampos(self):
        self.lineEdit1.clear()
        self.PlainDiagnostico.clear()
        self.PlainTratamiento.clear()
        self.PlainObservaciones.clear()
        self.TableCitasActivas.clearSelection()
        self.lineEdit1.setFocus()
        pass

    def cargar_detalles_diagnostico(self):
        try:
            # Obtener el ID de la cita seleccionada
            selected_index = self.TableCitasActivas.currentIndex()
            self.lineEdit1.setText(self.TableCitasActivas.model().index(selected_index.row(), 1).data() + " " + self.TableCitasActivas.model().index(selected_index.row(), 2).data())
           
           # Si el status de la cita es "Cancelada" o "Completada", no se puede registrar un diagnóstico
            if self.TableCitasActivas.model().index(selected_index.row(), 4).data() in ["cancelada", "programada"]:  # Estado de la cita
                self.PlainDiagnostico.clear()
                self.PlainTratamiento.clear()
                self.PlainObservaciones.clear()
                self.TableCitasActivas.clearSelection()
                self.lineEdit1.setFocus()
                return

            cita_id = self.TableCitasActivas.model().index(selected_index.row(), 0).data()
            print(f"ID de la cita seleccionada: {cita_id}")
            # Llamar al stored procedure para obtener los detalles del diagnóstico
            success, data = self.db_manager.DetallesDiagnostico(cita_id)
            if not success:
                QMessageBox.warning(self, "Error", data)
                return
        
            # Mostrar los detalles del diagnóstico en los campos de texto
            self.PlainDiagnostico.setPlainText(data[0])
            self.PlainTratamiento.setPlainText(data[1])
            self.PlainObservaciones.setPlainText(data[2])
        except Exception as e:
            # Mostrar un mensaje de error si ocurre una excepción
            #QMessageBox.warning(self, "Database", "Este registro no contiene un diagnóstico")
            self.PlainDiagnostico.clear()
            self.PlainTratamiento.clear()
            self.PlainObservaciones.clear()
            self.TableCitasActivas.clearSelection()
            self.lineEdit1.setFocus()
        pass
            
        
if __name__ == "__main__":
    app = QApplication([])
    Medico_window = WindowMedico()
    Medico_window.show()
    app.exec()
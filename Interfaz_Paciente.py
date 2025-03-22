# ↓↓↓↓↓↓↓
# Para abrir la interfaz de paciente, se debe ejecutar el archivo Main.py y luego iniciar sesión con un usuario de tipo paciente.
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from DatabaseManager import DatabaseManager

class WindowPaciente(QMainWindow):

    def __init__(self, user_data):
        super().__init__()

        # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

        self.user_data = user_data  # Datos del usuario que inició sesión
        self.id_paciente = user_data[0]  # ID del paciente
        self.id_Doctor = 0  # ID del médico seleccionado
        self.id_Cita_Paciente = 0  # ID del paciente seleccionado

        # Configuración de la ventana
        #self.resize(980, 422)
        self.setFixedSize(980, 422) # No se puede cambiar el tamaño de la ventana
        self.setWindowTitle('Consultorio Medico || Paciente')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.setWindowOpacity(0.90)  # Opacidad de la ventana
        self.setStyleSheet('background-color: rgb(0, 0, 0);')  # Color de fondo de la ventana
        
        self.cargar_medicos()  # Cargar los médicos al iniciar la ventana
        self.CargarUsuarioDetails()  # Cargar los detalles del usuario || ID del paciente
        self.CargarCitasActivas()  # Cargar las citas activas del paciente

    def create_widgets(self):
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(16, 48, 416, 344)
        self.groupBox1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.groupBox1.setTitle('Agendar Cita')
        self.lMedico = QLabel(self.groupBox1)
        self.lMedico.setGeometry(48, 96, 160, 24) # (48, 40, 104, 34)
        self.lMedico.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lMedico.setText('Medico: ')
        self.lFechadecita = QLabel(self.groupBox1)
        self.lFechadecita.setGeometry(16, 168, 152, 24)
        self.lFechadecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lFechadecita.setText('Fecha de cita:')
        self.lCITASACTIVAS = QLabel(self)
        self.lCITASACTIVAS.setGeometry(608, 16, 92, 24)
        self.lCITASACTIVAS.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lCITASACTIVAS.setText('CITAS ACTIVAS')
        self.lHoradecita = QLabel(self.groupBox1)
        self.lHoradecita.setGeometry(16, 208, 152, 34)
        self.lHoradecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lHoradecita.setText('Hora de cita:')

         # Label para mostrar el saludo
        self.lSaludo = QLabel(self)
        self.lSaludo.setGeometry(16, 8, 400, 24)
        self.lSaludo.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        # UserNAme (índice 1)
        self.lSaludo.setText(f" Bienvenido: {self.user_data[1]} ")  # Nombre de usuario


        # Tabla de citas activas del paciente || 03/15/2025 12:34
        self.TablaCitas = QTableView(self)
        self.TablaCitas.setGeometry(440, 48, 528, 296)
        self.TablaCitas.setFont(QFont('Segoe UI', 9))
        self.TablaCitas.setStyleSheet('color: rgb(255, 255, 255);')
        self.TablaCitas.setModel(QStandardItemModel())
        self.TablaCitas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.TablaCitas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.TablaCitas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.TablaCitas.horizontalHeader().setStretchLastSection(True)
        self.TablaCitas.verticalHeader().setVisible(False)
        self.TablaCitas.horizontalHeader().setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.TablaCitas.setStyleSheet('background-color: rgb(59, 7, 56);')
        #self.TablaCitas.clicked.connect(self.TablaCitas_clicked)

        # Boton cerrar sesion
        self.bCerrarSesion = QPushButton(self)
        self.bCerrarSesion.setGeometry(776, 360, 120, 40)
        self.bCerrarSesion.setFont(QFont('Segoe UI', 9))
        self.bCerrarSesion.setText('Cerrar Sesion')
        self.bCerrarSesion.clicked.connect(self.bCerrarSesion_clicked)
        self.bCerrarSesion.setStyleSheet('background-color: rgb(255, 0, 0);')

        # Boton confirmar cita
        self.bConfirmarCita = QPushButton(self.groupBox1)
        self.bConfirmarCita.setGeometry(32, 272, 344, 56)
        self.bConfirmarCita.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.bConfirmarCita.setStyleSheet('color: rgb(0, 0, 0);')
        self.bConfirmarCita.setStyleSheet('background-color: rgb(0, 255, 0);')
        self.bConfirmarCita.setText('Confirmar Cita')
        self.bConfirmarCita.clicked.connect(self.bConfirmarCita_clicked)

        # # Selector de especialidad
        # self.cmbEspecialidad = QComboBox(self.groupBox1)
        # self.cmbEspecialidad.setGeometry(168, 32, 216, 40)
        # self.cmbEspecialidad.setFont(QFont('Segoe UI', 9))
        # self.cmbEspecialidad.setModel(QStringListModel(['Medico General', 'Ginecologia', 'Pediatra', 'Odontologia', 'Psiquiatra', 'Psicologia', 'Urologo', 'Nefrologo']))

        # ComboBox para seleccionar el médico
        self.cmbEspecialidad = QComboBox(self.groupBox1)
        self.cmbEspecialidad.setGeometry(168, 32, 216, 40)
        self.cmbEspecialidad.setFont(QFont('Segoe UI', 9))
        self.cmbEspecialidad.setPlaceholderText("Seleccione un médico")
        self.cmbEspecialidad.currentIndexChanged.connect(self.ActualizarLabelMedico) # Actualizar el label del médico seleccionado

        self.lEspecialidad1 = QLabel(self.groupBox1)
        # Ajuste de geometria: X, Y, Ancho, Alto
        self.lEspecialidad1.setGeometry(8, 40, 160, 34) # (8, 96, 160, 24)
        self.lEspecialidad1.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lEspecialidad1.setText('Especialidad:')

        self.lCIRUJANO = QLabel(self.groupBox1)
        self.lCIRUJANO.setGeometry(168, 88, 160, 34)
        self.lCIRUJANO.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lCIRUJANO.setStyleSheet('color: rgb(23, 255, 237);')
        self.lCIRUJANO.setText('------')

        self.dte_Nacimiento = QDateEdit(self)
        self.dte_Nacimiento.setGeometry(176, 220, 208, 32)
        self.dte_Nacimiento.setFont(QFont('Segoe UI', 9))
        self.dte_Nacimiento.setCalendarPopup(True)
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.dte_Nacimiento.setMinimumDate(QDate(1970, 1, 1))
        self.dte_Nacimiento.setMaximumDate(QDate(2032, 1, 1))

        # Selector de hora de cita
        self.tme_HoraCita = QTimeEdit(self)
        self.tme_HoraCita.setGeometry(176, 260, 208, 32) # (16, 208, 152, 34)
        self.tme_HoraCita.setFont(QFont('Segoe UI', 9))
        #self.tme_HoraCita.setDisplayFormat('h:mm:ss AP')
        # formato de 24 horas
        self.tme_HoraCita.setTime(QTime.currentTime())
        self.tme_HoraCita.setDisplayFormat('HH:mm:ss AP')
        # MAXIMO Y MINIMO DE HORA DE CITA
        # self.tme_HoraCita.setMinimumTime(QTime(8, 0))
        # self.tme_HoraCita.setMaximumTime(QTime(18, 0))

        # Boton cancelar cita
        self.btnCancelarCita = QPushButton(self)
        self.btnCancelarCita.setGeometry(440, 352, 208, 40)
        self.btnCancelarCita.setFont(QFont('Segoe UI', 9))
        self.btnCancelarCita.setStyleSheet('background-color: rgb(245, 120, 11);')
        self.btnCancelarCita.setText('Cancelar Cita Seleccionada')
        self.btnCancelarCita.clicked.connect(self.CancelarCitaSeleccionada)

        pass

    def bCerrarSesion_clicked(self, checked):
        self.close()
        self.mostrar_ventana_login()
        pass

    def mostrar_ventana_login(self):
        """Muestra la ventana de inicio de sesión."""
        from Main import LogInWindow  # Importar la ventana de inicio de sesión
        self.ventana_login = LogInWindow()
        self.ventana_login.show()

    def bConfirmarCita_clicked(self, checked):
        
        if self.id_Doctor == 0:
            QMessageBox.critical(self, "Error", "Seleccione un médico.")
            return
        
        if self.tme_HoraCita.time() < QTime(8, 0) or self.tme_HoraCita.time() > QTime(18, 0):
             QMessageBox.critical(self, "Error", "La hora de la cita debe estar entre las 8:00 AM y las 6:00 PM.")
             return
        
        ID_Paciente = self.id_Cita_Paciente
        ID_Medico = self.id_Doctor
        Fecha_Hora = f"{self.dte_Nacimiento.date().toString('yyyy-MM-dd')} {self.tme_HoraCita.time().toString('HH:mm:ss')}"
        success, message = self.db_manager.agendar_cita(ID_Paciente, ID_Medico, Fecha_Hora)
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.CargarCitasActivas() # Actualizar la tabla de citas
            self.LimpiarCampos()
        else:
            QMessageBox.critical(self, "Error", message)

    def btnCancelarCita_clicked(self, checked):
        # ToDo insert source code here
        pass

    def ActualizarLabelMedico(self):
        # use consultoriomedico;
        # SELECT * FROM consultoriomedico.medicos where id_medico = 2;
        medicoID = self.cmbEspecialidad.currentIndex()
        success, medico = self.db_manager.obtener_medicos()
        if not success:
            QMessageBox.critical(self, "Error", medico)
            return
        self.id_Doctor = medico[medicoID][0]
        # Nombre y apellido del medico
        self.lCIRUJANO.setText(f"{medico[medicoID][1]} {medico[medicoID][2]}") # Nombre y apellido del medico [1] [2]
        #self.lCIRUJANO.setText(medico[medicoID][1]) # Nombre del medico [1]
        #print(medico[medicoID][1])
        
    def cargar_medicos(self):
        success, medicos = self.db_manager.obtener_medicos()
        if success:
            for medico in medicos:
                self.cmbEspecialidad.addItem(medico[3]) # Espesialidad del medico [3]
        else:
            QMessageBox.critical(self, "Error", medicos)
    
    def CargarUsuarioDetails(self):
        success, detalles_usuario = self.db_manager.obtener_detalles_usuario(self.id_paciente)
        if not success:
            QMessageBox.critical(self, "Error", detalles_usuario)
            return
        self.id_Cita_Paciente = detalles_usuario[4]  # ID del paciente
        
        pass

    def LimpiarCampos(self):
        self.cmbEspecialidad.setCurrentIndex(0)
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.tme_HoraCita.setTime(QTime.currentTime())
        pass

    def CargarCitasActivas(self):
        success, citas_activas = self.db_manager.cargar_citas_activas(self.id_Cita_Paciente)
        if not success:
            QMessageBox.critical(self, "Error", citas_activas)
            return
        # Configurar la tabla de citas
        model = QStandardItemModel()
        model.setColumnCount(6)
        model.setHorizontalHeaderLabels(["ID Cita", "Nombre Médico", "Apellido Médico", "Especialidad", "Fecha y Hora", "Estado"])
        self.TablaCitas.setModel(model)
        for cita in citas_activas:
            row = [
                QStandardItem(str(cita[0])),  # ID Cita
                QStandardItem(cita[1]),      # Nombre Médico
                QStandardItem(cita[2]),      # Apellido Médico
                QStandardItem(cita[3]),      # Especialidad
                QStandardItem(str(cita[4])),  # Fecha y Hora
                QStandardItem(cita[5])       # Estado
            ]
            model.appendRow(row)
        self.TablaCitas.resizeColumnsToContents()
        pass

    def CancelarCitaSeleccionada(self):
        selected_index = self.TablaCitas.currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Advertencia", "Seleccione una cita para cancelar.")
            return
        cita_id = self.TablaCitas.model().index(selected_index.row(), 0).data()
        confirmacion = QMessageBox.question(
            self, 
            "Cancelar Cita", 
            "¿Está seguro de que desea cancelar esta cita?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmacion == QMessageBox.StandardButton.Yes:
            success, message = self.db_manager.cancelar_cita(cita_id)
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.CargarCitasActivas()
            else:
                QMessageBox.critical(self, "Error", message)
        pass

if __name__ == "__main__":
    app = QApplication([])
    Paciente_window = WindowPaciente()
    Paciente_window.show()
    app.exec()
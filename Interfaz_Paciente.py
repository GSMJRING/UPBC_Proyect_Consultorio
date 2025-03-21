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

        # Configuración de la ventana
        self.resize(912, 422)
        self.setWindowTitle('Consultorio Medico || Paciente')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.cargar_medicos()  # Cargar los médicos al iniciar la ventana

    def create_widgets(self):
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(16, 48, 416, 344)
        self.groupBox1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.groupBox1.setTitle('Agendar Cita')
        self.lMedico = QLabel(self.groupBox1)
        self.lMedico.setGeometry(48, 40, 104, 34)
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
        self.lSaludo.setText(f" Bienvenido: {self.user_data[1]} ")  # Nombre y apellido


        # Tabla de citas activas del paciente || 03/15/2025 12:34
        self.TablaCitas = QTableView(self)
        self.TablaCitas.setGeometry(440, 48, 457, 296)
        self.TablaCitas.setFont(QFont('Segoe UI', 9))
        self.TablaCitas.setModel(QStandardItemModel())

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

        self.lCIRUJANO = QLabel(self.groupBox1)
        self.lCIRUJANO.setGeometry(168, 88, 160, 34)
        self.lCIRUJANO.setFont(QFont('Segoe UI Black', 16))
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
        self.tme_HoraCita.setDisplayFormat('HH:mm')
        # MAXIMO Y MINIMO DE HORA DE CITA
        self.tme_HoraCita.setMinimumTime(QTime(8, 0))
        self.tme_HoraCita.setMaximumTime(QTime(18, 0))

        # Boton cancelar cita
        self.btnCancelarCita = QPushButton(self)
        self.btnCancelarCita.setGeometry(440, 352, 208, 40)
        self.btnCancelarCita.setFont(QFont('Segoe UI', 9))
        self.btnCancelarCita.setStyleSheet('background-color: rgb(245, 120, 11);')
        self.btnCancelarCita.setText('Cancelar Cita Seleccionada')
        self.btnCancelarCita.clicked.connect(self.btnCancelarCita_clicked)
        #self.HoraCita.setGeometry(176, 208, 208, 32)
        #self.FechaCita.setGeometry(176, 160, 208, 32)
        self.lEspecialidad1 = QLabel(self.groupBox1)
        self.lEspecialidad1.setGeometry(8, 96, 160, 24)
        self.lEspecialidad1.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lEspecialidad1.setText('Especialidad:')

        pass

    def bCerrarSesion_clicked(self, checked):
        # ToDo insert source code here
        pass

    def bConfirmarCita_clicked(self, checked):
        # ToDo insert source code here
        pass

    def btnCancelarCita_clicked(self, checked):
        # ToDo insert source code here
        pass

    def cargar_medicos(self):
        """Carga los nombres de los médicos en el ComboBox."""
        success, medicos = self.db_manager.obtener_medicos()
        if success:
            self.cmbEspecialidad.clear()
            for medico in medicos:
                nombre_completo = f"{medico[1]} {medico[2]}"  # Nombre y apellido
                self.cmbEspecialidad.addItem(nombre_completo, medico[0])  # Guardar el ID del médico como dato
                self.lCIRUJANO.setText(medico[3])  # Especialidad del médico
        else:
            QMessageBox.critical(self, "Error", medicos)

if __name__ == "__main__":
    app = QApplication([])
    Paciente_window = WindowPaciente()
    Paciente_window.show()
    app.exec()
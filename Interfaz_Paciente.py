from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class WindowPaciente(QMainWindow):

    def __init__(self, user_data):
        super().__init__()
        self.resize(912, 394)
        self.user_data = user_data  # Datos del usuario que inició sesión
        self.id_paciente = user_data[0]  # ID del paciente
        self.setWindowTitle('Consultorio Medico || Paciente')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar

    def create_widgets(self):
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(16, 24, 416, 296)
        self.groupBox1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.groupBox1.setTitle('Agendar Cita')
        self.lEspecialidad = QLabel(self.groupBox1)
        self.lEspecialidad.setGeometry(24, 48, 160, 24)
        self.lEspecialidad.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lEspecialidad.setText('Especialidad:')
        self.lFechadecita = QLabel(self.groupBox1)
        self.lFechadecita.setGeometry(16, 112, 152, 24)
        self.lFechadecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lFechadecita.setText('Fecha de cita:')
        self.lCITASACTIVAS = QLabel(self)
        self.lCITASACTIVAS.setGeometry(608, 16, 92, 24)
        self.lCITASACTIVAS.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lCITASACTIVAS.setText('CITAS ACTIVAS')
        self.lHoradecita = QLabel(self.groupBox1)
        self.lHoradecita.setGeometry(16, 160, 152, 34)
        self.lHoradecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lHoradecita.setText('Hora de cita:')
         # Label para mostrar el saludo
        self.lSaludo = QLabel(self)
        self.lSaludo.setGeometry(16, 8, 400, 24)
        self.lSaludo.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        self.lSaludo.setText(f"Bienvenido, {self.user_data[1]} {self.user_data[2]}")  # Nombre y apellido


        # Tabla de citas activas del paciente || 03/15/2025 12:34
        self.TablaCitas = QTableView(self)
        self.TablaCitas.setGeometry(440, 48, 457, 265)
        self.TablaCitas.setFont(QFont('Segoe UI', 9))
        self.TablaCitas.setModel(QStandardItemModel())

        # Boton cerrar sesion
        self.bCerrarSesion = QPushButton(self)
        self.bCerrarSesion.setGeometry(776, 344, 120, 40)
        self.bCerrarSesion.setFont(QFont('Segoe UI', 9))
        self.bCerrarSesion.setText('Cerrar Sesion')
        self.bCerrarSesion.clicked.connect(self.bCerrarSesion_clicked)
        self.bCerrarSesion.setStyleSheet('background-color: rgb(255, 0, 0);')

        # Boton confirmar cita
        self.bConfirmarCita = QPushButton(self.groupBox1)
        self.bConfirmarCita.setGeometry(32, 216, 344, 56)
        self.bConfirmarCita.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.bConfirmarCita.setStyleSheet('color: rgb(0, 0, 0);')
        self.bConfirmarCita.setStyleSheet('background-color: rgb(0, 255, 0);')
        self.bConfirmarCita.setText('Confirmar Cita')
        self.bConfirmarCita.clicked.connect(self.bConfirmarCita_clicked)

        # Selector de especialidad
        self.cmbEspecialidad = QComboBox(self.groupBox1)
        self.cmbEspecialidad.setGeometry(168, 40, 216, 40)
        self.cmbEspecialidad.setFont(QFont('Segoe UI', 9))
        self.cmbEspecialidad.setModel(QStringListModel(['Medico General', 'Ginecologia', 'Pediatra', 'Odontologia', 'Psiquiatra', 'Psicologia', 'Urologo', 'Nefrologo']))

        # Selector de fecha de cita
        # self.FechaCita = QDateEdit(self.groupBox1)
        # self.FechaCita.setGeometry(176, 104, 208, 32)
        # self.FechaCita.setFont(QFont('Segoe UI', 9))
        # self.FechaCita.setDisplayFormat('m/d/yyyy')

        self.dte_Nacimiento = QDateEdit(self)
        self.dte_Nacimiento.setGeometry(176, 135, 208, 32)
        self.dte_Nacimiento.setFont(QFont('Segoe UI', 9))
        self.dte_Nacimiento.setCalendarPopup(True)
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.dte_Nacimiento.setMinimumDate(QDate(1970, 1, 1))
        self.dte_Nacimiento.setMaximumDate(QDate(2032, 1, 1))

        # Selector de hora de cita
        self.tme_HoraCita = QTimeEdit(self)
        self.tme_HoraCita.setGeometry(176, 190, 208, 32)
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
        self.btnCancelarCita.setGeometry(448, 320, 208, 40)
        self.btnCancelarCita.setFont(QFont('Segoe UI', 9))
        self.btnCancelarCita.setStyleSheet('background-color: rgb(245, 120, 11);')
        self.btnCancelarCita.setText('Cancelar Cita Seleccionada')
        self.btnCancelarCita.clicked.connect(self.btnCancelarCita_clicked)
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


if __name__ == "__main__":
    app = QApplication([])
    Paciente_window = WindowPaciente()
    Paciente_window.show()
    app.exec()

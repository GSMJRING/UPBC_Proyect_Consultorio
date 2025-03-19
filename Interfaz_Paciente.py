from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(912, 394)
        self.setWindowTitle('Consultorio Medico || Paciente')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()

    def create_widgets(self):
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(16, 24, 416, 296)
        self.groupBox1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.groupBox1.setTitle('Agendar Cita')
        self.lEspecialidad = QLabel(self.groupBox1)
        self.lEspecialidad.setGeometry(24, 48, 160, 24)
        self.lEspecialidad.setFont(QFont('Segoe UI Black', 16, QFont.Weight.Bold))
        self.lEspecialidad.setText('Especialidad:')

        # Tabla de citas activas del paciente || 03/15/2025 12:34
        self.TablaCitas = QTableView(self)
        self.TablaCitas.setGeometry(440, 48, 457, 265)
        self.TablaCitas.setFont(QFont('Segoe UI', 9))
        self.TablaCitas.setModel(QStandardItemModel())
        self.lFechadecita = QLabel(self.groupBox1)
        self.lFechadecita.setGeometry(16, 112, 152, 24)
        self.lFechadecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lFechadecita.setText('Fecha de cita:')
        self.lCITASACTIVAS = QLabel(self)
        self.lCITASACTIVAS.setGeometry(608, 16, 92, 24)
        self.lCITASACTIVAS.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lCITASACTIVAS.setText('CITAS ACTIVAS')
        # Boton cerrar sesion
        self.bCerrarSesion = QPushButton(self)
        self.bCerrarSesion.setGeometry(736, 336, 120, 40)
        self.bCerrarSesion.setFont(QFont('Segoe UI', 9))
        self.bCerrarSesion.setText('Cerrar Sesion')
        self.bCerrarSesion.clicked.connect(self.bCerrarSesion_clicked)
        self.bCerrarSesion.setStyleSheet('background-color: rgb(255, 0, 0);')
        # Boton confirmar cita
        self.bConfirmarCita = QPushButton(self.groupBox1)
        self.bConfirmarCita.setGeometry(24, 216, 344, 56)
        self.bConfirmarCita.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.bConfirmarCita.setStyleSheet('color: rgb(0, 0, 0);')
        # Cambiar color de letra a negro
        self.bConfirmarCita.setStyleSheet('background-color: rgb(0, 255, 0);')
        self.bConfirmarCita.setText('Confirmar Cita')
        self.bConfirmarCita.clicked.connect(self.bConfirmarCita_clicked)
        # Selector de especialidad
        self.cmbEspecialidad = QComboBox(self.groupBox1)
        self.cmbEspecialidad.setGeometry(168, 40, 216, 40)
        self.cmbEspecialidad.setFont(QFont('Segoe UI', 9))
        self.cmbEspecialidad.setModel(QStringListModel(['Medico General', 'Ginecologia', 'Pediatra', 'Odontologia', 'Psiquiatra', 'Psicologia', 'Urologo', 'Nefrologo']))
        # Selector de fecha de cita
        # self.dateEdit1 = QDateEdit(self.groupBox1)
        # self.dateEdit1.setGeometry(176, 104, 208, 32)
        # self.dateEdit1.setFont(QFont('Segoe UI', 9))
        # self.dateEdit1.setDisplayFormat('m/d/yyyy')

        self.dte_Nacimiento = QDateEdit(self)
        self.dte_Nacimiento.setGeometry(176, 135, 208, 32)
        self.dte_Nacimiento.setFont(QFont('Segoe UI', 9))
        self.dte_Nacimiento.setCalendarPopup(True)
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.dte_Nacimiento.setMinimumDate(QDate(1970, 1, 1))
        self.dte_Nacimiento.setMaximumDate(QDate(2032, 1, 1))

        # Selector de hora de cita
        # self.timeEdit1 = QTimeEdit(self.groupBox1)
        # self.timeEdit1.setGeometry(176, 160, 208, 32)
        # self.timeEdit1.setFont(QFont('Segoe UI', 9))
        # self.timeEdit1.setDisplayFormat('h:nn:ss AMPM')
        self.tme_HoraCita = QTimeEdit(self)
        self.tme_HoraCita.setGeometry(176, 190, 208, 32)
        self.tme_HoraCita.setFont(QFont('Segoe UI', 9))
        self.tme_HoraCita.setDisplayFormat('h:mm:ss AP')
        self.tme_HoraCita.setTime(QTime.currentTime())
        # MAXIMO Y MINIMO DE HORA DE CITA 
        self.tme_HoraCita.setMinimumTime(QTime(8, 0))
        self.tme_HoraCita.setMaximumTime(QTime(18, 0))

        # Labels
        self.lHoradecita = QLabel(self.groupBox1)
        self.lHoradecita.setGeometry(16, 160, 152, 34)
        self.lHoradecita.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lHoradecita.setText('Hora de cita:')
        pass

    def bCerrarSesion_clicked(self, checked):
        # ToDo insert source code here
        pass

    def bConfirmarCita_clicked(self, checked):
        # ToDo insert source code here
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

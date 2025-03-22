from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from DatabaseManager import DatabaseManager

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.resize(1388, 775)
        self.setFixedSize(1388, 775) 
        self.setWindowTitle('Consultorio Medico || Medico Especialista')
        self.setCentralWidget(QWidget(self))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.create_widgets()

    def create_widgets(self):
        self.GpCitas = QGroupBox(self)
        self.GpCitas.setGeometry(680, 72, 664, 616)
        self.GpCitas.setFont(QFont('Segoe UI', 9))
        self.GpCitas.setTitle('Resgistro de citas')
        self.GralData = QFrame(self)
        self.GralData.setGeometry(16, 16, 640, 208)
        self.GralData.setFont(QFont('Segoe UI', 9))
        self.GpDiagnostico = QGroupBox(self)
        self.GpDiagnostico.setGeometry(16, 232, 641, 457)
        self.GpDiagnostico.setFont(QFont('Segoe UI', 9))
        self.GpDiagnostico.setTitle('Diagnostico y Tratamiento')
        self.lblConsulEsp = QLabel(self.GralData)
        self.lblConsulEsp.setGeometry(112, 8, 392, 24)
        self.lblConsulEsp.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
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
        
        self.lineEdit1 = QLineEdit(self.GralData)
        self.lineEdit1.setGeometry(120, 160, 345, 33)
        self.lineEdit1.setFont(QFont('Segoe UI', 9))

        # Tablas de diagnostico y Entrada de texto
        self.PlainDiagnostico = QPlainTextEdit(self.GpDiagnostico)
        self.PlainDiagnostico.setGeometry(16, 32, 608, 256)
        self.PlainDiagnostico.setFont(QFont('Segoe UI', 9))

        self.TableCitasActivas = QTableView(self.GpCitas)
        self.TableCitasActivas.setGeometry(16, 32, 633, 569)
        self.TableCitasActivas.setFont(QFont('Segoe UI', 9))
        self.TableCitasActivas.setModel(QStandardItemModel())
        self.TableCitasActivas.setAlternatingRowColors(True)

        # Botones de accion de la aplicacion
        self.BtnDiagnostico = QToolButton(self.GpDiagnostico)
        self.BtnDiagnostico.setGeometry(16, 336, 160, 48)
        self.BtnDiagnostico.setFont(QFont('Segoe UI', 9))
        self.BtnDiagnostico.setText('Registrar Diagnostico')
        self.BtnDiagnostico.clicked.connect(self.BtnDiagnostico_clicked)

        self.BtnCancelarCita = QToolButton(self.GpDiagnostico)
        self.BtnCancelarCita.setGeometry(240, 336, 160, 48)
        self.BtnCancelarCita.setFont(QFont('Segoe UI', 9))
        self.BtnCancelarCita.setText('Cancelar Cita')
        self.BtnCancelarCita.clicked.connect(self.BtnCancelarCita_clicked)

        self.BtnReprogramar = QToolButton(self.GpDiagnostico)
        self.BtnReprogramar.setGeometry(456, 336, 160, 48)
        self.BtnReprogramar.setFont(QFont('Segoe UI', 9))
        self.BtnReprogramar.setText('Reprogramar Cita')
        self.BtnReprogramar.clicked.connect(self.BtnReprogramar_clicked)

        self.BtnCerrarSesion = QToolButton(self)
        self.BtnCerrarSesion.setGeometry(1184, 704, 160, 48)
        self.BtnCerrarSesion.setFont(QFont('Segoe UI', 9))
        self.BtnCerrarSesion.setText('Cerrar Sesion')
        self.BtnCerrarSesion.clicked.connect(self.BtnCerrarSesion_clicked)

        self.BtnBuscarPAciente = QToolButton(self.GralData)
        self.BtnBuscarPAciente.setGeometry(480, 160, 120, 32)
        self.BtnBuscarPAciente.setFont(QFont('Segoe UI', 9))
        self.BtnBuscarPAciente.setText('Buscar Paciente')
        self.BtnBuscarPAciente.clicked.connect(self.BtnBuscarPAciente_clicked)

        # Labels de cambio segun el inicio de sesion 
        self.LblEspecialidadDoc = QLabel(self.GralData)
        self.LblEspecialidadDoc.setGeometry(144, 104, 304, 29)
        self.LblEspecialidadDoc.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.LblEspecialidadDoc.setText('--------------------')
        self.LblMedicoEsp = QLabel(self.GralData)
        self.LblMedicoEsp.setGeometry(144, 64, 304, 29)
        self.LblMedicoEsp.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        self.LblMedicoEsp.setText('--------------------')
        pass

    def BtnDiagnostico_clicked(self, checked):
        # ToDo insert source code here
        pass

    def BtnCancelarCita_clicked(self, checked):
        # ToDo insert source code here
        pass

    def BtnReprogramar_clicked(self, checked):
        # ToDo insert source code here
        pass

    def BtnCerrarSesion_clicked(self, checked):
        self.close()
        self.mostrar_ventana_login

    def BtnBuscarPAciente_clicked(self, checked):
        # ToDo insert source code here
        pass

    def mostrar_ventana_login(self):
        """Muestra la ventana de inicio de sesión."""
        from Main import LogInWindow  # Importar la ventana de inicio de sesión
        self.ventana_login = LogInWindow()
        self.ventana_login.show()

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
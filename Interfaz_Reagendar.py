from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSignal  # Importar pyqtSignal para crear señales
from mysql.connector import connect
from DatabaseManager import DatabaseManager 

class WindowReagendar(QMainWindow):

# Definir una señal que se emitirá cuando la cita se reagende
    cita_reagendada = pyqtSignal()

    def __init__(self, ID_Cita, ID_Nombre):
        super().__init__()
         
         # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

        self.ID_Cita = ID_Cita 
        self.ID_Nombre = ID_Nombre

        #self.resize(249, 327)
        self.setFixedSize(249, 327)
        self.setWindowTitle('Reagendar Cita')
        self.setCentralWidget(QWidget(self))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.setWindowOpacity(0.90)  # Opacidad de la ventana
        self.create_widgets()

    def create_widgets(self):
        # Fecha y hora 
        self.NewDate = QDateEdit(self)
        self.NewDate.setGeometry(40, 112, 152, 32)
        self.NewDate.setFont(QFont('Segoe UI', 9))
        self.NewDate.setCalendarPopup(True)
        self.NewDate.setDate(QDate.currentDate())
        self.NewDate.setMinimumDate(QDate.currentDate())
        self.NewDate.setMaximumDate(QDate(2032, 1, 1))
        #self.NewDate.setDisplayFormat('m/d/yyyy')
        # Hora 
        self.NewTime = QTimeEdit(self)
        self.NewTime.setGeometry(40, 192, 152, 32)
        self.NewTime.setFont(QFont('Segoe UI', 9))
        self.NewTime.setTime(QTime.currentTime())
        self.NewTime.setMinimumTime(QTime(8, 0))
        self.NewTime.setMaximumTime(QTime(18, 0))
        self.NewTime.setDisplayFormat('HH:mm:ss AP')

        self.lSeleccionarnuevafecha = QLabel(self)
        self.lSeleccionarnuevafecha.setGeometry(48, 80, 132, 24)
        self.lSeleccionarnuevafecha.setFont(QFont('Segoe UI', 9))
        self.lSeleccionarnuevafecha.setText('Seleccionar nueva fecha')
        self.lSeleccionarnuevahoradecita = QLabel(self)
        self.lSeleccionarnuevahoradecita.setGeometry(32, 160, 184, 24)
        self.lSeleccionarnuevahoradecita.setFont(QFont('Segoe UI', 9))
        self.lSeleccionarnuevahoradecita.setText('Seleccionar nueva hora de cita')
        self.lPaciente = QLabel(self)
        self.lPaciente.setGeometry(16, 32, 72, 24)
        self.lPaciente.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        self.lPaciente.setText('Paciente:')

        # Label del paciente seleccionado
        self.lblPaciente = QLabel(self)
        self.lblPaciente.setGeometry(96, 32, 128, 24)
        self.lblPaciente.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        #self.lblPaciente.setText('------------------')
        self.lblPaciente.setText(self.ID_Nombre)
        # Botones
        self.bConfirmar = QPushButton(self)
        self.bConfirmar.setGeometry(24, 264, 89, 41)
        self.bConfirmar.setFont(QFont('Segoe UI', 9))
        self.bConfirmar.setText('Confirmar')
        self.bConfirmar.clicked.connect(self.bConfirmar_clicked)

        self.bCancelar = QPushButton(self)
        self.bCancelar.setGeometry(144, 264, 89, 41)
        self.bCancelar.setFont(QFont('Segoe UI', 9))
        self.bCancelar.setText('Cancelar')
        self.bCancelar.clicked.connect(self.bCancelar_clicked)
        pass

    def bConfirmar_clicked(self, checked):
        """Reagenda la cita con la nueva fecha y hora seleccionada."""
        # Preguntar si esta seguro de reagendar la cita
        if QMessageBox.question(self, 'Reagendar Cita', '¿Está seguro de reagendar la cita?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            # Obtener la nueva fecha y hora seleccionada
            nueva_fecha_hora = f"{self.NewDate.date().toString('yyyy-MM-dd')} {self.NewTime.time().toString('HH:mm:ss')}"
            success, message = self.db_manager.ReagendarCita(self.ID_Cita, nueva_fecha_hora)
            if success:
                QMessageBox.information(self, 'Cita Reagendada', 'La cita ha sido reagendada con éxito.')
                # Emitir la señal para notificar que la cita se ha reagendado
                self.cita_reagendada.emit() 
                self.close()
                self.db_manager.disconnect()
            else:
                QMessageBox.warning(self, 'Error', f'Error al reagendar la cita: {message}')
                self.db_manager.disconnect()
        else:
            QMessageBox.information(self, 'Reagendar Cita', 'Accion cancelada por el usuario.')
            self.close()
            self.db_manager.disconnect()
            
        pass

    def bCancelar_clicked(self, checked):
        # Cerrar la ventana
        self.close()
        self.db_manager.disconnect()
        pass

if __name__ == "__main__":
    app = QApplication([])
    Reagendar_window = WindowReagendar()
    Reagendar_window.show()
    app.exec()

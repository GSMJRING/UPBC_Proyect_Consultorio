from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(912, 429)
        self.setWindowTitle('Consultorio Medico || Paciente')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()

    def create_widgets(self):
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(16, 16, 416, 400)
        self.groupBox1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.groupBox1.setTitle('Agendar Cita')
        self.lEspecialidad = QLabel(self.groupBox1)
        self.lEspecialidad.setGeometry(16, 32, 80, 24)
        self.lEspecialidad.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lEspecialidad.setText('Especialidad:')
        
        # Tabla de citas activas del paciente || 03/15/2025 12:34
        self.TablaCitas = QTableView(self)
        self.TablaCitas.setGeometry(440, 48, 457, 265)
        self.TablaCitas.setFont(QFont('Segoe UI', 9))
        self.TablaCitas.setModel(QStandardItemModel())
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

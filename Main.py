# Aplicacion ejecutada desde GitHub
# Consultorio Medico
# Nota: Es importante instalar las liberiarias de PyQt6 y mysql-connector-python
# pip install PyQt6 mysql-connector-python
#
# Crear el instalador de la aplicacion (pip install pyinstaller)
# pyinstaller --onefile --noconsole --icon=Consultorio\Login.ico Main.py
# Ventana de inicio de sesion
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap # Importar la clase QPixmap para la imagen de inicio de sesion
from ConsultorioMedico_Admin import WindowAdmin  # Importar la clase WindowAdmin
from Interfaz_Paciente import WindowPaciente  # Importar la clase WindowPaciente
from Interfaz_Medico import WindowMedico  # Importar la clase WindowMedico
from easteregg import SnakeGame  # Importar la clase SnakeGame


# Conexion a base de datos
#from ConsultorioMedico_LogIn_Function import *  # Importar la clase LoginSystem base de datos || Database ConsultorioMedico
from DatabaseManager import DatabaseManager  # Importar la clase DatabaseManager
# Clase de inicio de sesion

class LogInWindow(QMainWindow):
    # Apartado de dimensiones de ventana y titulo
    def __init__(self):
        super().__init__()
        # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

        self.setWindowIcon(QIcon('C:\Consultorio\Login.ico'))  # Icono de la ventana de la aplicacion
        self.LogInRutaIMG = "C:\Consultorio\DM_Login.png" # Ruta de la imagen de inicio de sesion
        
        #self.resize(305, 416)
        self.setFixedSize(305, 416) # No se puede cambiar el tamaño de la ventana
        self.setWindowTitle('Consultorio Medico || LogIn')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.txt_User.setFocus()  # Enfocar el campo de usuario

    # Apartado de contenido de la ventana
    def create_widgets(self):
        # Imagen de inicio de sesion
        pixmap1 = QPixmap(self.LogInRutaIMG)
        self.PICLogin = QLabel(self)
        self.PICLogin.setPixmap(pixmap1)
        self.PICLogin.setGeometry(72, 16, 160, 129)
        self.PICLogin.setScaledContents(True)
        
        # Boton de inicio de sesion.
        self.bLogIn = QPushButton(self)
        self.bLogIn.setGeometry(24, 360, 120, 40)
        self.bLogIn.setFont(QFont('Segoe UI', 9))
        self.bLogIn.setText('LogIn')
        self.bLogIn.clicked.connect(self.bLogIn_clicked)

        # TextBox de usuario y password
        self.txt_User = QLineEdit(self)
        self.txt_User.setGeometry(64, 200, 193, 33)
        self.txt_User.setFont(QFont('Segoe UI', 9))
        self.txt_User.setMaxLength(20) # Limitar la cantidad de caracteres a 20

        # TXT Password esta configurado para contraseña
        self.txt_Pass = QLineEdit(self)
        self.txt_Pass.setGeometry(64, 288, 193, 33)
        self.txt_Pass.setFont(QFont('Segoe UI', 9))
        self.txt_Pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_Pass.setMaxLength(20) # Limitar la cantidad de caracteres a 20

        # Boton Cancel
        self.bCancel = QPushButton(self)
        self.bCancel.setGeometry(160, 360, 120, 40)
        self.bCancel.setFont(QFont('Segoe UI', 9))
        self.bCancel.setText('Cancel')
        self.bCancel.clicked.connect(self.bCancel_clicked)

        # Label de usuario y password
        self.lUser = QLabel(self)
        self.lUser.setGeometry(64, 168, 80, 24)
        self.lUser.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lUser.setText('User')

        self.lPassword = QLabel(self)
        self.lPassword.setGeometry(64, 248, 105, 34)
        self.lPassword.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.lPassword.setText('Password')

        # Si presiona la tecla Enter en el campo de contraseña, se inicia sesión
        self.txt_Pass.returnPressed.connect(self.bLogIn.click)

        pass

    # Funciones al presionar los botones
    def bLogIn_clicked(self, checked):
        # Solicitar credenciales al usuario
        # Cambio de datos || 03/15/2025 5:02 || MS
        username = self.txt_User.text()
        password = self.txt_Pass.text()

        if self.txt_User.text() == "" or self.txt_Pass.text() == "":
            QMessageBox.warning(self, "Error", "Por favor, ingrese su usuario y contraseña.")
            return
        
        if username == "snake" and password == "snake":
            QMessageBox.information(self, "Bienvenido al juego !", "Easter Egg!")
            self.Eagsteregg()
            return
        
        else:
            # Validar las credenciales
            # Aqui estaba el error Andres → 03/15/2025 12:34
            is_valid,user_data = self.db_manager.validate_user(username, password)

            if is_valid:
                if  user_data[3] == "administrador":
                    QMessageBox.information(self, "Inicio de sesión exitoso", "¡Bienvenido!")
                    self.open_admin_window(user_data)  # Pasar los datos del usuario a la ventana del administrador
                elif user_data[3] == "paciente":
                    QMessageBox.information(self, "Inicio de sesión exitoso", "¡Bienvenido!")
                    self.open_paciente_window(user_data) # Pasar los datos del usuario a la ventana del paciente
                else:
                    QMessageBox.information(self, "Inicio de sesión exitoso", "¡Bienvenido!")
                    self.open_medico_window(user_data) # Pasar los datos del usuario a la ventana del Doctor
            else:
                QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos.")
                self.txt_Pass.clear()  # Limpiar el campo de contraseña
                self.txt_Pass.setFocus()  # Enfocar el campo de contraseña
                return

            # Cerrar la conexión a la base de datos antes de iniciar la ventana siguiente
            self.db_manager.disconnect()

    def bCancel_clicked(self, checked):
        app = QApplication.instance()
        if app:
            app.quit()  # Close the application
        else:
            self.close()  # Fallback to just closing the window if no QApplication instance

    def open_admin_window(self,user_data):
        """Abre la ventana de administrador."""
        #self.admin_window = WindowAdmin(db_manager=self.login_system)
        self.db_manager.disconnect()
        self.admin_window = WindowAdmin(user_data=user_data) # Pasar el Administrador user
        self.admin_window.show()
        self.close()

    def open_paciente_window(self, user_data): # Mandar datos de usuario a la ventana del paciente
        """Abre la ventana de paciente."""
        self.db_manager.disconnect()
        self.paciente_window = WindowPaciente(user_data=user_data)
        self.paciente_window.show()
        self.close()

    def open_medico_window(self, user_data): # Mandar datos de usuario a la ventana del medico
        """Abre la ventana de medico."""
        self.db_manager.disconnect()
        self.medico_window = WindowMedico(user_data=user_data)
        self.medico_window.show()
        self.close()

    def Eagsteregg(self):
        self.snake_game = SnakeGame()
        self.snake_game.show()


# MENU
if __name__ == "__main__":
    app = QApplication([])
    login_window = LogInWindow()
    login_window.show()
    app.exec()
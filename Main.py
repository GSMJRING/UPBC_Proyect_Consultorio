# Aplicacion ejecutada desde GitHub
# Consultorio Medico
# Nota: Es importante instalar las liberiarias de PyQt6 y mysql-connector-python
# pip install PyQt6 mysql-connector-python
#
# Ventana de inicio de sesion
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap # Importar la clase QPixmap para la imagen de inicio de sesion
from ConsultorioMedico_Admin import WindowAdmin  # Importar la clase WindowAdmin
# Conexion a base de datos
#from ConsultorioMedico_LogIn_Function import *  # Importar la clase LoginSystem base de datos || Database ConsultorioMedico
from DatabaseManager import DatabaseManager  # Importar la clase DatabaseManager
# Clase de inicio de sesion


class LogInWindow(QMainWindow):
    # Apartado de dimensiones de ventana y titulo
    def __init__(self):
        super().__init__()
        # # Configuración de la conexión a la base de datos
        # self.host = "localhost"  # Cambia esto si tu base de datos está en otro servidor
        # self.user = "root"  # Cambia esto por tu usuario de MySQL
        # self.password = "Capgemini2008"  # Cambia esto por tu contraseña de MySQL
        # self.database = "Consultoriomedico"  # Version actual
        # self.login_system = LoginSystem(self.host, self.user, self.password, self.database)

        # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

        self.setWindowIcon(QIcon('C:\Consultorio\Login.ico'))  # Icono de la ventana de la aplicacion
        self.LogInRutaIMG = "C:\Consultorio\DM_Login.png" # Ruta de la imagen de inicio de sesion

        self.resize(305, 416)
        self.setWindowTitle('Consultorio Medico || LogIn')
        self.setCentralWidget(QWidget(self))
        self.create_widgets()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar

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

        pass

    # Funciones al presionar los botones
    def bLogIn_clicked(self, checked):
        # Solicitar credenciales al usuario
        username = self.txt_User.text()
        password = self.txt_Pass.text()

        if self.txt_User.text() == "" or self.txt_Pass.text() == "":
            QMessageBox.warning(self, "Error", "Por favor, ingrese su usuario y contraseña.")
            return
        else:
            # Validar las credenciales
            #is_valid, user_data = self.login_system.validate_user(username, password)
            # Aqui estaba el error Andres → 03/15/2025 12:34
            is_valid,user_data = self.db_manager.validate_user(username, password)

            if is_valid:
                QMessageBox.information(self, "Inicio de sesión exitoso", "¡Bienvenido!")
                self.open_admin_window()  # Abrir la ventana de administrador
            else:
                QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos.")
                self.txt_Pass.clear()  # Limpiar el campo de contraseña
                self.txt_Pass.setFocus()  # Enfocar el campo de contraseña
                return

            # Cerrar la conexión a la base de datos antes de iniciar la ventana siguiente
            # self.login_system.close_connection()
            self.db_manager.disconnect()

    def bCancel_clicked(self, checked):
        app = QApplication.instance()
        if app:
            app.quit()  # Close the application
        else:
            self.close()  # Fallback to just closing the window if no QApplication instance

    def open_admin_window(self):
        """Abre la ventana de administrador."""
        #self.admin_window = WindowAdmin(db_manager=self.login_system)
        self.admin_window = WindowAdmin()
        self.admin_window.show()
        self.close()


# MENU
if __name__ == "__main__":
    app = QApplication([])
    login_window = LogInWindow()
    login_window.show()
    app.exec()
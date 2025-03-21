#Ventana de Administrador
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap
from hashlib import sha256 # Encruptador de contraseña basado en SHA256
from DatabaseManager import DatabaseManager

class WindowAdmin(QMainWindow):
    def __init__(self, user_data):
        super().__init__()

        # Nuevo modo de conexion a base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.connect()

        self.setWindowIcon(QIcon('C:\Consultorio\Admin_Logo.ico'))  # Icono de la ventana de la aplicacion
        self.RutaImagen = "C:\Consultorio\DM_Admin.png" # Ruta de la imagen

        self.user_data = user_data  # Datos del usuario que inició sesión
        #self.resize(952, 632)
        self.setFixedSize(952, 632) # No se puede cambiar el tamaño de la ventana
        self.setWindowTitle('Consultorio Medico || Administrador')
        self.setCentralWidget(QWidget(self))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)  # No se puede maximizar
        self.setWindowOpacity(0.90)  # Opacidad de la ventana
        self.setStyleSheet('background-color: rgb(0, 0, 0);')  # Color de fondo de la ventana
        self.create_widgets()


    def create_widgets(self):
        # Logo de la aplicacion || Cambia la ruta de la imagen dependiendo de la ubicacion
        pixmap= QPixmap(self.RutaImagen)
        self.LogoIMG = QLabel(self)
        self.LogoIMG.setPixmap(pixmap)
        self.LogoIMG.setGeometry(448, 48, 129, 129)
        self.LogoIMG.setScaledContents(True)

        # Boton agregar usuario
        self.bAgregarUsuario = QPushButton(self)
        self.bAgregarUsuario.setGeometry(32, 512, 169, 65)
        self.bAgregarUsuario.setFont(QFont('Segoe UI', 9))
        self.bAgregarUsuario.setText('Agregar Usuario')
        self.bAgregarUsuario.clicked.connect(self.bAgregarUsuario_clicked)

        # Boton Cancelar
        self.bCerrarventana = QPushButton(self)
        self.bCerrarventana.setGeometry(768, 520, 169, 65)
        self.bCerrarventana.setFont(QFont('Segoe UI', 9))
        self.bCerrarventana.setText('Cerrar ventana')
        self.bCerrarventana.clicked.connect(self.bCerrarventana_clicked)

        # Boton ver usuarios activos
        self.bVerUsuarios = QPushButton(self)
        self.bVerUsuarios.setGeometry(592, 520, 169, 65)
        self.bVerUsuarios.setFont(QFont('Segoe UI', 9))
        self.bVerUsuarios.setText('Ver Usuarios')
        self.bVerUsuarios.clicked.connect(self.bVerUsuarios_clicked)

        # List view - mostrar usuarios activos
        self.ListUSers = QListView(self)
        self.ListUSers.setGeometry(592, 24, 320, 472)
        self.ListUSers.setFont(QFont('Segoe UI', 9))
        # Conectar la selección de un usuario en la lista
        self.ListUSers.clicked.connect(self.cargar_detalles_usuario)

        # Labels generales
        self.lNombre = QLabel(self)
        self.lNombre.setGeometry(40, 256, 120, 24)
        self.lNombre.setFont(QFont('Segoe UI', 9))
        self.lNombre.setText('Nombre:')

        self.lApellido = QLabel(self)
        self.lApellido.setGeometry(40, 296, 120, 24)
        self.lApellido.setFont(QFont('Segoe UI', 9))
        self.lApellido.setText('Apellido:')

        self.lTelefono = QLabel(self)
        self.lTelefono.setGeometry(40, 344, 120, 24)
        self.lTelefono.setFont(QFont('Segoe UI', 9))
        self.lTelefono.setText('Telefono:')

        self.lEmail = QLabel(self)
        self.lEmail.setGeometry(40, 384, 120, 24)
        self.lEmail.setFont(QFont('Segoe UI', 9))
        self.lEmail.setText('Email:')

        # GroupBox - Informacion de usuario
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(24, 56, 424, 176)
        self.groupBox1.setFont(QFont('Segoe UI', 9))
        self.groupBox1.setTitle('Informacion de Usuario')

        self.txt_User = QLineEdit(self.groupBox1)
        self.txt_User.setGeometry(128, 64, 160, 33)
        self.txt_User.setFont(QFont('Segoe UI', 9))
        self.txt_User.setMaxLength(10) # Limitar la cantidad de caracteres a 10

        self.txt_Password = QLineEdit(self.groupBox1)
        self.txt_Password.setGeometry(128, 104, 160, 33)
        self.txt_Password.setFont(QFont('Segoe UI', 9))
        self.txt_Password.setEchoMode(QLineEdit.EchoMode.Password)

        self.lUsuario1 = QLabel(self.groupBox1)
        self.lUsuario1.setGeometry(32, 72, 80, 24)
        self.lUsuario1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lUsuario1.setText('Usuario:')

        self.lTipodeUsuario1 = QLabel(self.groupBox1)
        self.lTipodeUsuario1.setGeometry(16, 24, 94, 24)
        self.lTipodeUsuario1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lTipodeUsuario1.setText('Tipo de Usuario :')

        self.lPassword1 = QLabel(self.groupBox1)
        self.lPassword1.setGeometry(32, 112, 80, 24)
        self.lPassword1.setFont(QFont('Segoe UI', 9, QFont.Weight.Bold))
        self.lPassword1.setText('Password:')

        # ComboBox de seleccion tipo de usuario
        self.cmb_UserType = QComboBox(self.groupBox1)
        self.cmb_UserType.setGeometry(128, 24, 160, 32)
        self.cmb_UserType.setFont(QFont('Segoe UI', 9))
        self.cmb_UserType.setModel(QStringListModel(['Paciente', 'Doctor', 'Administrador']))
        self.cmb_UserType.currentTextChanged.connect(self.update_label)

        # ComboBox de especialidades
        self.cmbEspecialidad = QComboBox(self)
        self.cmbEspecialidad.setGeometry(176, 416, 264, 32)
        self.cmbEspecialidad.setFont(QFont('Segoe UI', 9))
        self.cmbEspecialidad.setModel(QStringListModel(['Medico General', 'Ginecologia', 'Pediatra', 'Odontologia', 'Psiquiatra', 'Psicologia', 'Urologo', 'Nefrologo']))
        self.cmbEspecialidad.hide() # Ocultar de forma inicial

        # LBL de funcion automatica en cuestion del CMB
        self.label1 = QLabel(self)
        self.label1.setGeometry(40, 424, 120, 24)
        self.label1.setFont(QFont('Segoe UI', 9))
        self.label1.setText('Fecha de Nacimiento:')

        # Campos de texto
        self.txt_Nombre = QLineEdit(self)
        self.txt_Nombre.setGeometry(176, 248, 273, 25)
        self.txt_Nombre.setFont(QFont('Segoe UI', 9))

        self.txt_Apellido = QLineEdit(self)
        self.txt_Apellido.setGeometry(176, 288, 273, 25)
        self.txt_Apellido.setFont(QFont('Segoe UI', 9))

        self.txt_Telefono = QLineEdit(self)
        self.txt_Telefono.setGeometry(176, 336, 273, 25)
        self.txt_Telefono.setFont(QFont('Segoe UI', 9))

        self.txt_Email = QLineEdit(self)
        self.txt_Email.setGeometry(176, 376, 273, 25)
        self.txt_Email.setFont(QFont('Segoe UI', 9))

        self.dte_Nacimiento = QDateEdit(self)
        self.dte_Nacimiento.setGeometry(176, 416, 273, 33)
        self.dte_Nacimiento.setFont(QFont('Segoe UI', 9))
        self.dte_Nacimiento.setCalendarPopup(True)
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.dte_Nacimiento.setMinimumDate(QDate(1970, 1, 1))
        self.dte_Nacimiento.setMaximumDate(QDate(2032, 1, 1))
        # Boton eliminar usuario
        self.bEliminarUsuario = QPushButton(self)
        self.bEliminarUsuario.setGeometry(400, 520, 136, 48)
        self.bEliminarUsuario.setFont(QFont('Segoe UI', 9))
        self.bEliminarUsuario.setText('Eliminar Usuario')
        self.bEliminarUsuario.clicked.connect(self.bEliminarUsuario_clicked)
        # Boton actualizar usuario
        self.bActualizarUsuario = QPushButton(self)
        self.bActualizarUsuario.setGeometry(216, 512, 169, 65)
        self.bActualizarUsuario.setFont(QFont('Segoe UI', 9))
        self.bActualizarUsuario.setText('Actualizar Usuario')
        self.bActualizarUsuario.clicked.connect(self.bActualizarUsuario_clicked)
        # Nota de usuario || Password
        self.lblNotificacionPWS = QLabel(self.groupBox1)
        self.lblNotificacionPWS.setGeometry(32, 144, 376, 24)
        self.lblNotificacionPWS.setFont(QFont('Segoe UI', 7))
        # Cambiar color de texto a azul
        self.lblNotificacionPWS.setStyleSheet("color: lightblue;")
        self.lblNotificacionPWS.setText('* Si se requiere actualizar el usuario: El cambio de password es necesario. ')

        # Label de usuario logeado
        self.lAdministrator = QLabel(self)
        self.lAdministrator.setGeometry(16, 8, 312, 24)
        self.lAdministrator.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        self.lAdministrator.setText(f" Bienvenido: {self.user_data[1]} ")  # Nombre y apellido
        #pass

    def update_label(self, text):
        if text == "Paciente":
            self.label1.setText("Fecha de Nacimiento:")
            self.label1.show()
            self.dte_Nacimiento.show()
            #self.txt_Especialidad.hide()
            self.cmbEspecialidad.hide()
        elif text == "Doctor":
            self.label1.setText("Especialidad:")
            self.label1.show()
            self.dte_Nacimiento.hide()
            #self.txt_Especialidad.show()
            self.cmbEspecialidad.show()
        else:  # Administrador
            self.label1.hide()
            self.dte_Nacimiento.hide()
           # self.txt_Especialidad.hide()
            self.cmbEspecialidad.hide()

    def bAgregarUsuario_clicked(self): # Funcion para agregar un usuario
        nombre_usuario = self.txt_User.text()
        contrasena = self.txt_Password.text()
        rol = self.cmb_UserType.currentText().lower()
        nombre = self.txt_Nombre.text()
        apellido = self.txt_Apellido.text()
        telefono = self.txt_Telefono.text()
        email = self.txt_Email.text()
        fecha_nacimiento = self.dte_Nacimiento.date().toString("yyyy-MM-dd") if rol == "paciente" else None
        #especialidad = self.txt_Especialidad.text() if rol == "doctor" else None
        especialidad = self.cmbEspecialidad.currentText() if rol == "doctor" else None # Se cambia a combobox || 03/15/2025 4:34 PM || MS

        success, message = self.db_manager.agregar_usuario(
            nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento, especialidad
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.bVerUsuarios_clicked()  # Actualizar la lista de usuarios
            self.LimpiarCampos() # Limpiar los campos
        else:
            QMessageBox.critical(self, "Error", message)

    def bCerrarventana_clicked(self):
        QApplication.instance().quit()  # Cerrar la aplicacion

    def bVerUsuarios_clicked(self):
        success, usuarios = self.db_manager.obtener_usuarios_activos()
        if success:
            model = QStringListModel()
            # Columnas seleccionadas: ID, Nombre, UserType
            model.setStringList([f"{u[0]} {u[1]} ({u[2]})" for u in usuarios])
            self.ListUSers.setModel(model)
        else:
            QMessageBox.critical(self, "Error", usuarios)

    def bEliminarUsuario_clicked(self, checked):
        # ToDo insert source code here
        selected_index = self.ListUSers.currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Advertencia", "Seleccione un usuario para eliminar.")
            return

        if QMessageBox.question(self, "Eliminar usuario", "¿Está seguro de que desea eliminar este usuario?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return

        usuario_id = selected_index.data().split()[0]
        success, message = self.db_manager.eliminar_usuario(usuario_id)
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.bVerUsuarios_clicked()
            self.LimpiarCampos()
        else:
            QMessageBox.critical(self, "Error", message)

        # #usuario_id = self.ListUSers.model().data(selected_index, Qt.DisplayRole).split()[0]
        # usuario_id = selected_index.data().split()[0]

        # success, message = self.db_manager.eliminar_usuario(usuario_id)
        # if success:
        #     QMessageBox.information(self, "Éxito", message)
        #     self.bVerUsuarios_clicked()  # Actualizar la lista de usuarios
        #     self.LimpiarCampos()
        # else:
        #     QMessageBox.critical(self, "Error", message)

    def bActualizarUsuario_clicked(self):
        """Actualiza la información del usuario seleccionado."""
        selected_index = self.ListUSers.currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Advertencia", "Seleccione un usuario para actualizar.")
            return

        #usuario_id = self.ListUSers.model().data(selected_index, Qt.DisplayRole).split()[0]
        usuario_id = selected_index.data().split()[0]

        nombre_usuario = self.txt_User.text()
        # Actualizar contraseña solo si se ha ingresado una nueva
        contrasena = self.txt_Password.text() if self.txt_Password.text() else None
        rol = self.cmb_UserType.currentText().lower()
        nombre = self.txt_Nombre.text()
        apellido = self.txt_Apellido.text()
        telefono = self.txt_Telefono.text()
        email = self.txt_Email.text()
        #self.dte_Nacimiento.setDate(detalles[7])  # fecha_nacimiento
        fecha_nacimiento = self.dte_Nacimiento.date().toString("yyyy-MM-dd") if rol == "paciente" else None
        #especialidad = self.txt_Especialidad.text() if rol == "doctor" else None
        especialidad = self.cmbEspecialidad.currentText() if rol == "doctor" else None

        success, message = self.db_manager.actualizar_usuario(
            usuario_id, nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento, especialidad
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.bVerUsuarios_clicked()
            self.LimpiarCampos()
        else:
            QMessageBox.critical(self, "Error", message)

    def cargar_detalles_usuario(self):
        """Carga los detalles del usuario seleccionado en los controles."""
        selected_index = self.ListUSers.currentIndex()  # Obtener el índice seleccionado
        if not selected_index.isValid():
            return

        # Obtener el ID del usuario seleccionado
        usuario_id = selected_index.data().split()[0]

        # Obtener los detalles del usuario desde la base de datos
        success, detalles = self.db_manager.obtener_detalles_usuario(usuario_id)
        if not success:
            QMessageBox.critical(self, "Error", detalles)
            return

        # Mostrar los detalles del usuario en los controles
        self.txt_User.setText(detalles[1])  # nombre_usuario (índice 1)
        self.cmb_UserType.setCurrentText(detalles[3].capitalize())  # rol (índice 3)

        # Mostrar la contraseña hasheada (índice 2)
        #self.txt_Password.setText(sha256(detalles[2].encode()).hexdigest())
        self.txt_Password.setPlaceholderText("PASSWORD HASHEADA")

        # Mostrar detalles según el rol del usuario
        if detalles[3] == "paciente":  # Verificar el rol (índice 3)
            self.txt_Nombre.setText(detalles[6])  # nombre_paciente (índice 6)
            self.txt_Apellido.setText(detalles[7])  # apellido_paciente (índice 7)
            self.dte_Nacimiento.setDate(detalles[8])  # fecha_nacimiento (índice 8)
            self.txt_Telefono.setText(detalles[9])  # telefono_paciente (índice 9)
            self.txt_Email.setText(detalles[10])  # email_paciente (índice 10)
        elif detalles[3] == "doctor":  # Verificar el rol (índice 3)
            self.txt_Nombre.setText(detalles[11])  # nombre_medico (índice 11)
            self.txt_Apellido.setText(detalles[12])  # apellido_medico (índice 12)
            self.cmbEspecialidad.setCurrentText(detalles[13])  # especialidad (índice 13)
            self.txt_Telefono.setText(detalles[14])  # telefono_medico (índice 14)
            self.txt_Email.setText(detalles[15])  # email_medico (índice 15)
        elif detalles[3] == "administrador":  # Verificar el rol (índice 3)
            # Si el rol es administrador, limpiar los campos
            self.txt_Nombre.setText("")
            self.txt_Apellido.setText("")
            self.txt_Telefono.setText("")
            self.txt_Email.setText("")
            self.dte_Nacimiento.setDate(QDate.currentDate())

    def LimpiarCampos(self): # Funcion para limpiar los campos
        self.cmb_UserType.setCurrentIndex(0)
        self.cmbEspecialidad.setCurrentIndex(0)
        self.ListUSers.clearSelection()
        self.txt_User.clear()
        self.txt_Password.clear()
        self.txt_Nombre.clear()
        self.txt_Apellido.clear()
        self.txt_Telefono.clear()
        self.txt_Email.clear()
        #self.txt_Especialidad.clear()
        self.dte_Nacimiento.setDate(QDate.currentDate())
        self.cmb_UserType.setFocus()

if __name__ == "__main__":
    app = QApplication([])

    # Crear y mostrar la ventana principal
    admin_window = WindowAdmin() # Pasar la instancia de DatabaseManager
    admin_window.show()

    # Ejecutar la aplicación
    app.exec()
import mysql.connector 
from mysql.connector import Error
from hashlib import sha256 # Encruptador de contraseña basado en SHA256
#from ConsultorioMedico_LogIn_Function import * # Importar la clase LoginSystem base de datos || Database ConsultorioMedico

class DatabaseManager:
    # Conexion a la base de datos || Credenciales de acceso
    # def __init__(self, host, user, password, database):
    #     self.host = host
    #     self.user = user
    #     self.password = password
    #     self.database = database
    #     self.connection = None
    
    def __init__(self):
        # Configuración de la conexión a la base de datos
        self.host="localhost" # PAra que el Dan se conecte a la base de datos usar "localhost:3306"
        self.user="root"
        #self.password="Castro10!Aboytes" # Dan
        self.password="Capgemini2008" # Marco
        #self.password="Aurora120601@" # Robbie
        #self.password="Carlos9828!" # Carlos
        self.database="consultoriomedico"
        self.connection = None
         
    
    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
    
# Consultorio_Funcion || Login System
    def validate_user(self, username, input_password): # Validacion de usuario (Inicio de sesion)
        """Valida las credenciales de un usuario."""
        # Hashear la contraseña proporcionada por el usuario
        hashed_input_password = sha256(input_password.encode()).hexdigest()
        cursor = self.connection.cursor()

        # Consulta para verificar si el usuario existe y la contraseña es válida
        query = "SELECT * FROM Usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        cursor.execute(query, (username, hashed_input_password))
        result = cursor.fetchone()

        if result:
            return True, result  # Devuelve True y los datos del usuario si las credenciales son válidas
        else:
            return False, None  # Devuelve False si las contraseñas no coinciden
# _________________________________________________________________________________________________________________________
# Storeprocedures MySQL

    def agregar_usuario(self, nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento=None, especialidad=None):
        """Llama al stored procedure para agregar un nuevo usuario."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc(
                "AgregarUsuario",
                (nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento, especialidad)
            )
            self.connection.commit()
            cursor.close()
            return True, "Usuario agregado correctamente."
        except Error as e:
            return False, f"No se pudo agregar el usuario: {e}"

    def obtener_usuarios_activos(self):
        """Llama al stored procedure para obtener la lista de usuarios activos."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("ObtenerUsuariosActivos")
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            cursor.close()
            return True, resultados
        except Error as e:
            return False, f"No se pudo obtener la lista de usuarios: {e}"

    def eliminar_usuario(self, usuario_id):
        """Llama al stored procedure para eliminar un usuario."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("EliminarUsuario", (usuario_id,))
            self.connection.commit()
            cursor.close()
            return True, "Usuario eliminado correctamente."
        except Error as e:
            return False, f"No se pudo eliminar el usuario: {e}"
        
    def obtener_detalles_usuario(self, usuario_id):
        """Llama al stored procedure para obtener los detalles de un usuario."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("ObtenerDetallesUsuario", (usuario_id,))
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchone()
            cursor.close()
            return True, resultados
        except Error as e:
            return False, f"No se pudo obtener los detalles del usuario: {e}"

    def actualizar_usuario(self, usuario_id, nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento=None, especialidad=None):
        """Llama al stored procedure para actualizar un usuario."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc(
                "ActualizarUsuario",
                (usuario_id, nombre_usuario, contrasena, rol, nombre, apellido, telefono, email, fecha_nacimiento, especialidad)
            )
            self.connection.commit()
            cursor.close()
            return True, "Usuario actualizado correctamente."
        except Error as e:
            return False, f"No se pudo actualizar el usuario: {e}"
        
    # Combobox de especialidades en la interfaz de médico
    def obtener_medicos(self):
        """Llama al stored procedure para obtener la lista de médicos."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("ObtenerMedicos")
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            cursor.close()
            return True, resultados
        except Error as e:
            return False, f"No se pudo obtener la lista de médicos: {e}"
        
    def agendar_cita(self, id_paciente, id_medico, fecha_hora):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("CrearCita", (id_paciente, id_medico, fecha_hora))
            self.connection.commit()
            cursor.close()
            return True, "Cita agendada exitosamente."
        except Exception as e:
            return False, f"Error al agendar la cita: {e}"
    
    def ReagendarCita(self, cita_id, nueva_fecha_hora):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("ReagendarCita", (cita_id, nueva_fecha_hora))
            self.connection.commit()
            cursor.close()
            return True, "Cita reagendada exitosamente."
        except Exception as e:
            return False, f"Error al reagendar la cita: {e}"
        
    def cargar_citas_activas(self, id_paciente):
            """Obtiene las citas activas del paciente y las muestra en la tabla."""
            try:
                cursor = self.connection.cursor()
                cursor.callproc("ConsultarCitasActivasPaciente", (id_paciente,))
                resultados = []
                for result in cursor.stored_results():
                    resultados = result.fetchall()
                cursor.close()
                return True, resultados
            except Error as e:
                return False, f"No se pudieron cargar las citas activas: {e}"
 
    def cancelar_cita(self, cita_id):
        """Cancela la cita seleccionada por el paciente."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("CancelarCita", (cita_id,))
            self.connection.commit()
            cursor.close()
            return True, "Cita cancelada exitosamente."
        except Exception as e:
            return False, f"No se pudo cancelar la cita: {e}"
    
    def cargar_citas_medico(self, id_medico):
        """Carga las citas del médico en la tabla."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc("ConsultarCitasMedico", (id_medico,))
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            cursor.close()
            return True, resultados
        except Error as e:
            return False, f"No se pudieron cargar las citas: {e}"
        
    
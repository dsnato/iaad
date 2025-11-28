import re
from datetime import datetime
import mysql.connector
from mysql.connector import Error


class ValidationError(Exception):
    pass


class MySQLDB:
    def __init__(self, host='localhost', user='root', password='', database=None, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        if self.conn and getattr(self.conn, 'is_connected', lambda: False)():
            return self.conn
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=False,
            )
            return self.conn
        except Error as e:
            raise

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass

    def _execute(self, sql, params=None, fetchone=False, fetchall=False, commit=False):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return None
        except Error as e:
            try:
                conn.rollback()
            except Exception:
                pass
            raise
        finally:
            cursor.close()

    # --- Validations ---
    def validate_cpf(self, cpf: str):
        if cpf is None:
            raise ValidationError('CPF é obrigatório')
        pattern = r'^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
        if not re.match(pattern, cpf):
            raise ValidationError('CPF inválido. Formato obrigatório: XXX.XXX.XXX-XX')

    def validate_email(self, email: str):
        if email is None or email == '':
            return True
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(pattern, email):
            raise ValidationError('E-mail em formato inválido')

    def validate_phone(self, phone: str):
        if phone is None or phone == '':
            return True
        patterns = [
            r'^\([0-9]{2}\)\s*[0-9]{4}-[0-9]{4}$',
            r'^\([0-9]{2}\)\s*[0-9]{5}-[0-9]{4}$',
        ]
        if not any(re.match(p, phone) for p in patterns):
            raise ValidationError('Telefone em formato inválido. Exemplos: (81) 3042-1112 ou (81) 99999-9999')

    def _parse_datetime(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, str):
            try:
                # Accept both date and datetime-like strings
                dt = datetime.fromisoformat(value)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                # try common MySQL datetime format
                return value
        return value

    # --- Clientes (Paciente) CRUD ---
    def get_clientes(self):
        sql = """
        SELECT CpfPaciente AS cpf, NomePac AS nome, DataNascimento AS data_nascimento,
               Genero AS genero, Telefone AS telefone, Email AS email
        FROM Paciente
        ORDER BY NomePac
        """
        return self._execute(sql, fetchall=True)

    def create_cliente(self, cpf: str, nome: str, data_nascimento: str, genero: str = None, telefone: str = None, email: str = None):
        self.validate_cpf(cpf)
        self.validate_email(email)
        self.validate_phone(telefone)
        sql = "INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (cpf, nome, data_nascimento, genero, telefone, email)
        try:
            self._execute(sql, params=params, commit=True)
            return cpf
        except Error:
            raise

    def update_cliente(self, cpf: str, nome: str = None, data_nascimento: str = None, genero: str = None, telefone: str = None, email: str = None):
        # Only update provided fields
        if not any([nome, data_nascimento, genero, telefone, email]):
            return False
        if telefone:
            self.validate_phone(telefone)
        if email:
            self.validate_email(email)
        parts = []
        params = []
        if nome:
            parts.append('NomePac = %s'); params.append(nome)
        if data_nascimento:
            parts.append('DataNascimento = %s'); params.append(data_nascimento)
        if genero:
            parts.append('Genero = %s'); params.append(genero)
        if telefone is not None:
            parts.append('Telefone = %s'); params.append(telefone)
        if email is not None:
            parts.append('Email = %s'); params.append(email)
        sql = f"UPDATE Paciente SET {', '.join(parts)} WHERE CpfPaciente = %s"
        params.append(cpf)
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_cliente(self, cpf: str):
        sql = "DELETE FROM Paciente WHERE CpfPaciente = %s"
        try:
            self._execute(sql, params=(cpf,), commit=True)
            return True
        except Error:
            raise

    # --- Pedidos (Consulta) CRUD ---
    def get_pedidos(self):
        sql = """
        SELECT c.CodCli, cl.NomeCli AS clinica_nome, c.CodMed, m.NomeMed AS medico_nome,
               c.CpfPaciente, p.NomePac AS paciente_nome, c.Data_Hora
        FROM Consulta c
        LEFT JOIN Clinica cl ON c.CodCli = cl.CodCli
        LEFT JOIN Medico m ON c.CodMed = m.CodMed
        LEFT JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        ORDER BY c.Data_Hora DESC
        """
        return self._execute(sql, fetchall=True)

    def get_pedido_por_id(self, codcli: str, codmed: str, cpf: str, data_hora):
        data_hora = self._parse_datetime(data_hora)
        sql = "SELECT * FROM Consulta WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        return self._execute(sql, params=(codcli, codmed, cpf, data_hora), fetchone=True)

    def create_pedido(self, codcli: str, codmed: str, cpf: str, data_hora):
        # validate formats
        self.validate_cpf(cpf)
        data_hora = self._parse_datetime(data_hora)
        sql = "INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES (%s, %s, %s, %s)"
        try:
            self._execute(sql, params=(codcli, codmed, cpf, data_hora), commit=True)
            return (codcli, codmed, cpf, data_hora)
        except Error:
            raise

    def update_pedido(self, old_keys: tuple, new_values: dict):
        # old_keys = (codcli, codmed, cpf, data_hora)
        # new_values may contain keys: CodCli, CodMed, CpfPaciente, Data_Hora
        if not old_keys or len(old_keys) != 4:
            raise ValueError('old_keys deve ser (CodCli, CodMed, CpfPaciente, Data_Hora)')
        set_parts = []
        params = []
        allowed = {'CodCli', 'CodMed', 'CpfPaciente', 'Data_Hora'}
        for k, v in new_values.items():
            if k not in allowed:
                continue
            if k == 'CpfPaciente':
                self.validate_cpf(v)
            if k == 'Data_Hora':
                v = self._parse_datetime(v)
            set_parts.append(f"{k} = %s")
            params.append(v)
        if not set_parts:
            return False
        sql = f"UPDATE Consulta SET {', '.join(set_parts)} WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        params.extend(list(old_keys))
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_pedido(self, codcli: str, codmed: str, cpf: str, data_hora):
        data_hora = self._parse_datetime(data_hora)
        sql = "DELETE FROM Consulta WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        try:
            self._execute(sql, params=(codcli, codmed, cpf, data_hora), commit=True)
            return True
        except Error:
            raise

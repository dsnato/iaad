from datetime import datetime, date
import re
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class ValidationError(Exception):
    pass


class MySQLDB:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.database = database or os.getenv('DB_NAME', 'consultas_medicas')
        self.port = port or int(os.getenv('DB_PORT', 3306))
        self.conn = None

    def connect(self):
        """Establish and return a MySQL connection (reuses if já conectado)."""
        if self.conn is not None:
            try:
                if getattr(self.conn, "is_connected", lambda: False)():
                    return self.conn
            except Exception:
                # attempt to recreate connection if is_connected check fails
                self.conn = None

        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=False
            )
            return self.conn

        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            finally:
                self.conn = None

    def _execute(self, sql, params=None, fetchone=False, fetchall=False, commit=False):
        """
        Helper to execute queries.
        - params: tuple or dict
        - fetchone/fetchall: choose result mode
        - commit: commit if True
        Returns rows (list of dict) or single dict for fetchone or None.
        """
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
        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao executar consulta: {str(e)}")
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    # --- Validations ---
    def validate_cpf(self, cpf: str):
        if cpf is None:
            raise ValidationError("CPF é obrigatório.")
        pattern = r'^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
        if not re.match(pattern, cpf):
            raise ValidationError("CPF inválido. Formato obrigatório: XXX.XXX.XXX-XX")
        return True

    def validate_email(self, email: str):
        if email is None or email == '':
            return True
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(pattern, email):
            raise ValidationError("E-mail inválido.")
        return True

    def validate_phone(self, phone: str):
        if phone is None or phone == '':
            return True
        pattern = r'^\([0-9]{2}\)\s*[0-9]{4,5}-[0-9]{4}$'
        if not re.match(pattern, phone):
            raise ValidationError("Telefone inválido. Formato esperado: (DD) XXXX-XXXX ou (DD) XXXXX-XXXX")
        return True

    def _parse_datetime(self, value):
        """Normalize input datetime/date/string to Python datetime object."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt
                except Exception:
                    continue
            try:
                return datetime.fromisoformat(value)
            except Exception:
                raise ValidationError("Formato de data/hora inválido. Use YYYY-MM-DD HH:MM:SS")
        raise ValidationError("Tipo de data/hora inválido.")

    # --- Clientes (Paciente) CRUD ---
    def get_clientes(self):
        sql = """
        SELECT
            CpfPaciente AS cpf,
            NomePac AS nome,
            DataNascimento AS data_nascimento,
            Genero AS genero,
            Telefone AS telefone,
            Email AS email
        FROM Paciente
        ORDER BY NomePac
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def create_cliente(
        self, cpf: str, nome: str, data_nascimento: str,
        genero: str = None, telefone: str = None, email: str = None
    ):
        self.validate_cpf(cpf)
        self.validate_email(email)
        self.validate_phone(telefone)
        dt = self._parse_datetime(data_nascimento)
        sql = """
        INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self._execute(
                sql,
                params=(cpf, nome, dt.date().isoformat(),
                        genero or '', telefone or '', email or ''),
                commit=True
            )
            return True
        except Error:
            raise

    def update_cliente(
        self, cpf: str, nome: str = None, data_nascimento: str = None,
        genero: str = None, telefone: str = None, email: str = None
    ):
        if not cpf:
            raise ValidationError("CPF do cliente obrigatório para atualização.")
        if email is not None:
            self.validate_email(email)
        if telefone is not None:
            self.validate_phone(telefone)
        if data_nascimento is not None:
            dt = self._parse_datetime(data_nascimento)
            data_nascimento = dt.date().isoformat()
        sets = []
        params = []
        if nome is not None:
            sets.append("NomePac = %s")
            params.append(nome)
        if data_nascimento is not None:
            sets.append("DataNascimento = %s")
            params.append(data_nascimento)
        if genero is not None:
            sets.append("Genero = %s")
            params.append(genero)
        if telefone is not None:
            sets.append("Telefone = %s")
            params.append(telefone)
        if email is not None:
            sets.append("Email = %s")
            params.append(email)
        if not sets:
            return 0
        sql = f"UPDATE Paciente SET {', '.join(sets)} WHERE CpfPaciente = %s"
        params.append(cpf)
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_cliente(self, cpf: str):
        if not cpf:
            raise ValidationError("CPF do cliente obrigatório para exclusão.")
        sql = "DELETE FROM Paciente WHERE CpfPaciente = %s"
        try:
            self._execute(sql, params=(cpf,), commit=True)
            return True
        except Error:
            raise

    # --- Pedidos (Consulta) CRUD ---
    def get_pedidos(self):
        sql = """
        SELECT
            c.CodCli AS CodCli,
            cl.NomeCli AS clinica_nome,
            c.CodMed AS CodMed,
            m.NomeMed AS medico_nome,
            c.CpfPaciente AS CpfPaciente,
            p.NomePac AS paciente_nome,
            c.Data_Hora AS Data_Hora
        FROM Consulta c
        LEFT JOIN Clinica cl ON c.CodCli = cl.CodCli
        LEFT JOIN Medico m ON c.CodMed = m.CodMed
        LEFT JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        ORDER BY c.Data_Hora
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_pedido_por_id(self, codcli: str, codmed: str, cpf: str, data_hora):
        if not (codcli and codmed and cpf and data_hora):
            raise ValidationError("Chave completa do pedido é obrigatória.")
        dt = self._parse_datetime(data_hora)
        sql = """
        SELECT
            CodCli, CodMed, CpfPaciente, Data_Hora
        FROM Consulta
        WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s
        """
        row = self._execute(sql, params=(codcli, codmed, cpf, dt.strftime("%Y-%m-%d %H:%M:%S")), fetchone=True)
        return row

    def create_pedido(self, codcli: str, codmed: str, cpf: str, data_hora):
        if not (codcli and codmed and cpf and data_hora):
            raise ValidationError("Todos os campos do pedido são obrigatórios.")
        dt = self._parse_datetime(data_hora)
        sql = """
        INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self._execute(sql, params=(codcli, codmed, cpf, dt.strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            return True
        except Error:
            raise

    def update_pedido(self, old_keys: tuple, new_values: dict):
        if not old_keys or len(old_keys) != 4:
            raise ValidationError("old_keys deve conter (codcli, codmed, cpf, data_hora).")
        codcli_old, codmed_old, cpf_old, data_hora_old = old_keys
        dt_old = self._parse_datetime(data_hora_old)
        sets = []
        params = []
        if 'codcli' in new_values:
            sets.append("CodCli = %s")
            params.append(new_values['codcli'])
        if 'codmed' in new_values:
            sets.append("CodMed = %s")
            params.append(new_values['codmed'])
        if 'cpf' in new_values:
            sets.append("CpfPaciente = %s")
            params.append(new_values['cpf'])
        if 'data_hora' in new_values:
            dt_new = self._parse_datetime(new_values['data_hora'])
            sets.append("Data_Hora = %s")
            params.append(dt_new.strftime("%Y-%m-%d %H:%M:%S"))
        if not sets:
            return 0
        sql = (
            f"UPDATE Consulta SET {', '.join(sets)} "
            "WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s "
            "AND Data_Hora = %s"
        )
        params.extend([codcli_old, codmed_old, cpf_old,
                       dt_old.strftime("%Y-%m-%d %H:%M:%S")])
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_pedido(self, codcli: str, codmed: str, cpf: str, data_hora):
        if not (codcli and codmed and cpf and data_hora):
            raise ValidationError("Chave completa do pedido é obrigatória.")
        dt = self._parse_datetime(data_hora)
        sql = "DELETE FROM Consulta WHERE CodCli = %s AND CodMed = %s AND CpfPaciente = %s AND Data_Hora = %s"
        try:
            self._execute(sql, params=(codcli, codmed, cpf, dt.strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            return True
        except Error:
            raise

    # --- Clinica CRUD ---
    def _validate_codcli(self, codcli: str):
        if not codcli:
            raise ValidationError("CodCli é obrigatório.")
        return True

    def get_clinicas(self):
        sql = """
        SELECT
            CodCli AS codcli,
            NomeCli AS nome,
            Endereco AS endereco,
            Telefone AS telefone,
            Email AS email
        FROM Clinica
        ORDER BY NomeCli
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_clinica_por_id(self, codcli: str):
        self._validate_codcli(codcli)
        sql = (
            "SELECT CodCli AS codcli, NomeCli AS nome, Endereco AS endereco, "
            "Telefone AS telefone, Email AS email FROM Clinica WHERE CodCli = %s"
        )
        row = self._execute(sql, params=(codcli,), fetchone=True)
        return row

    def create_clinica(self, codcli: str, nome: str, endereco: str = None, telefone: str = None, email: str = None):
        self._validate_codcli(codcli)
        self.validate_email(email)
        self.validate_phone(telefone)
        sql = "INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES (%s, %s, %s, %s, %s)"
        try:
            self._execute(sql, params=(codcli, nome, endereco or '', telefone or '', email or ''), commit=True)
            return True
        except Error:
            raise

    def update_clinica(self, codcli: str, nome: str = None, endereco: str = None, telefone: str = None, email: str = None):
        self._validate_codcli(codcli)
        if email is not None:
            self.validate_email(email)
        if telefone is not None:
            self.validate_phone(telefone)
        sets = []
        params = []
        if nome is not None:
            sets.append("NomeCli = %s")
            params.append(nome)
        if endereco is not None:
            sets.append("Endereco = %s")
            params.append(endereco)
        if telefone is not None:
            sets.append("Telefone = %s")
            params.append(telefone)
        if email is not None:
            sets.append("Email = %s")
            params.append(email)
        if not sets:
            return 0
        sql = f"UPDATE Clinica SET {', '.join(sets)} WHERE CodCli = %s"
        params.append(codcli)
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_clinica(self, codcli: str):
        self._validate_codcli(codcli)
        sql = "DELETE FROM Clinica WHERE CodCli = %s"
        try:
            self._execute(sql, params=(codcli,), commit=True)
            return True
        except Error:
            raise

    # --- Medico CRUD ---
    def _validate_codmed(self, codmed: str):
        if not codmed:
            raise ValidationError("CodMed é obrigatório.")
        return True

    def get_medicos(self):
        sql = """
        SELECT
            CodMed AS codmed,
            NomeMed AS nome,
            Especialidade AS especialidade,
            Telefone AS telefone,
            Email AS email
        FROM Medico
        ORDER BY NomeMed
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_medico_por_id(self, codmed: str):
        self._validate_codmed(codmed)
        sql = (
            "SELECT CodMed AS codmed, NomeMed AS nome, "
            "Especialidade AS especialidade, Telefone AS telefone, "
            "Email AS email FROM Medico WHERE CodMed = %s"
        )
        row = self._execute(sql, params=(codmed,), fetchone=True)
        return row

    def create_medico(self, codmed: str, nome: str, especialidade: str = None, telefone: str = None, email: str = None):
        self._validate_codmed(codmed)
        self.validate_email(email)
        self.validate_phone(telefone)
        sql = "INSERT INTO Medico (CodMed, NomeMed, Especialidade, Telefone, Email) VALUES (%s, %s, %s, %s, %s)"
        try:
            self._execute(sql, params=(codmed, nome, especialidade or '', telefone or '', email or ''), commit=True)
            return True
        except Error:
            raise

    def update_medico(
        self, codmed: str, nome: str = None, especialidade: str = None,
        telefone: str = None, email: str = None
    ):
        self._validate_codmed(codmed)
        if email is not None:
            self.validate_email(email)
        if telefone is not None:
            self.validate_phone(telefone)
        sets = []
        params = []
        if nome is not None:
            sets.append("NomeMed = %s")
            params.append(nome)
        if especialidade is not None:
            sets.append("Especialidade = %s")
            params.append(especialidade)
        if telefone is not None:
            sets.append("Telefone = %s")
            params.append(telefone)
        if email is not None:
            sets.append("Email = %s")
            params.append(email)
        if not sets:
            return 0
        sql = f"UPDATE Medico SET {', '.join(sets)} WHERE CodMed = %s"
        params.append(codmed)
        try:
            self._execute(sql, params=tuple(params), commit=True)
            return True
        except Error:
            raise

    def delete_medico(self, codmed: str):
        self._validate_codmed(codmed)
        sql = "DELETE FROM Medico WHERE CodMed = %s"
        try:
            self._execute(sql, params=(codmed,), commit=True)
            return True
        except Error:
            raise

    # ========================================
    # CONSULTAS NÃO TRIVIAIS - BONIFICAÇÃO
    # ========================================

    def get_estatisticas_por_clinica(self):
        """
        Retorna estatísticas de consultas por clínica.
        Usa: COUNT, GROUP BY, LEFT JOIN
        """
        sql = """
        SELECT
            cl.CodCli AS codigo_clinica,
            cl.NomeCli AS nome_clinica,
            COUNT(c.CodCli) AS total_consultas,
            COUNT(DISTINCT c.CodMed) AS total_medicos_atendendo,
            COUNT(DISTINCT c.CpfPaciente) AS total_pacientes_atendidos
        FROM Clinica cl
        LEFT JOIN Consulta c ON cl.CodCli = c.CodCli
        GROUP BY cl.CodCli, cl.NomeCli
        ORDER BY total_consultas DESC
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_medicos_mais_atendimentos(self, limit=10):
        """
        Ranking de médicos com mais consultas agendadas.
        Usa: COUNT, GROUP BY, ORDER BY, LIMIT
        """
        sql = """
        SELECT
            m.CodMed AS codigo_medico,
            m.NomeMed AS nome_medico,
            m.Especialidade AS especialidade,
            COUNT(c.CodMed) AS total_consultas,
            COUNT(DISTINCT c.CpfPaciente) AS pacientes_unicos
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        GROUP BY m.CodMed, m.NomeMed, m.Especialidade
        ORDER BY total_consultas DESC
        LIMIT %s
        """
        rows = self._execute(sql, params=(limit,), fetchall=True)
        return rows or []

    def get_consultas_por_periodo(self, data_inicio, data_fim):
        """
        Consultas em um período específico com informações completas.
        Usa: BETWEEN, manipulação de datas, múltiplos JOINs
        """
        dt_inicio = self._parse_datetime(data_inicio)
        dt_fim = self._parse_datetime(data_fim)

        sql = """
        SELECT
            c.Data_Hora AS data_hora,
            cl.NomeCli AS clinica,
            m.NomeMed AS medico,
            m.Especialidade AS especialidade,
            p.NomePac AS paciente,
            p.Telefone AS telefone_paciente,
            DATEDIFF(c.Data_Hora, NOW()) AS dias_ate_consulta
        FROM Consulta c
        INNER JOIN Clinica cl ON c.CodCli = cl.CodCli
        INNER JOIN Medico m ON c.CodMed = m.CodMed
        INNER JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        WHERE c.Data_Hora BETWEEN %s AND %s
        ORDER BY c.Data_Hora
        """
        rows = self._execute(sql, params=(dt_inicio, dt_fim), fetchall=True)
        return rows or []

    def get_pacientes_por_genero(self):
        """
        Estatísticas demográficas dos pacientes.
        Usa: COUNT, GROUP BY, agregação
        """
        sql = """
        SELECT
            COALESCE(NULLIF(Genero, ''), 'Não informado') AS genero,
            COUNT(*) AS total_pacientes,
            ROUND(AVG(YEAR(CURDATE()) - YEAR(DataNascimento)), 1) AS idade_media,
            MIN(YEAR(CURDATE()) - YEAR(DataNascimento)) AS idade_minima,
            MAX(YEAR(CURDATE()) - YEAR(DataNascimento)) AS idade_maxima
        FROM Paciente
        GROUP BY Genero
        ORDER BY total_pacientes DESC
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_consultas_por_mes(self, ano=None):
        """
        Distribuição de consultas por mês.
        Usa: DATE_FORMAT, COUNT, GROUP BY, manipulação de datas
        """
        if ano is None:
            ano = datetime.now().year

        sql = """
        SELECT
            DATE_FORMAT(Data_Hora, '%%Y-%%m') AS mes,
            MONTH(Data_Hora) AS numero_mes,
            MONTHNAME(Data_Hora) AS nome_mes,
            COUNT(*) AS total_consultas,
            COUNT(DISTINCT CodMed) AS medicos_ativos,
            COUNT(DISTINCT CpfPaciente) AS pacientes_atendidos
        FROM Consulta
        WHERE YEAR(Data_Hora) = %s
        GROUP BY DATE_FORMAT(Data_Hora, '%%Y-%%m'), MONTH(Data_Hora), MONTHNAME(Data_Hora)
        ORDER BY numero_mes
        """
        rows = self._execute(sql, params=(ano,), fetchall=True)
        return rows or []

    def get_especialidades_mais_procuradas(self):
        """
        Ranking de especialidades médicas mais procuradas.
        Usa: COUNT, GROUP BY, ORDER BY
        """
        sql = """
        SELECT
            COALESCE(NULLIF(m.Especialidade, ''), 'Não especificada') AS especialidade,
            COUNT(c.CodMed) AS total_consultas,
            COUNT(DISTINCT c.CpfPaciente) AS pacientes_unicos,
            COUNT(DISTINCT m.CodMed) AS medicos_especialidade
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        GROUP BY m.Especialidade
        ORDER BY total_consultas DESC
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_taxa_ocupacao_por_dia_semana(self):
        """
        Análise de ocupação por dia da semana.
        Usa: DAYOFWEEK, DAYNAME, COUNT, AVG, GROUP BY
        """
        sql = """
        SELECT
            DAYOFWEEK(Data_Hora) AS numero_dia,
            DAYNAME(Data_Hora) AS dia_semana,
            COUNT(*) AS total_consultas,
            COUNT(DISTINCT CodCli) AS clinicas_ativas,
            ROUND(COUNT(*) / COUNT(DISTINCT DATE(Data_Hora)), 2) AS media_consultas_por_dia
        FROM Consulta
        GROUP BY DAYOFWEEK(Data_Hora), DAYNAME(Data_Hora)
        ORDER BY numero_dia
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_pacientes_sem_consulta(self):
        """
        Pacientes cadastrados que nunca tiveram consulta.
        Usa: LEFT JOIN com filtro IS NULL
        """
        sql = """
        SELECT
            p.CpfPaciente AS cpf,
            p.NomePac AS nome,
            p.Telefone AS telefone,
            p.Email AS email,
            YEAR(CURDATE()) - YEAR(p.DataNascimento) AS idade,
            DATEDIFF(CURDATE(), p.DataNascimento) AS dias_cadastrado
        FROM Paciente p
        LEFT JOIN Consulta c ON p.CpfPaciente = c.CpfPaciente
        WHERE c.CpfPaciente IS NULL
        ORDER BY p.NomePac
        """
        rows = self._execute(sql, fetchall=True)
        return rows or []

    def get_consultas_proximas(self, dias=7):
        """
        Consultas agendadas para os próximos N dias.
        Usa: DATE_ADD, CURDATE, manipulação de datas
        """
        sql = """
        SELECT
            c.Data_Hora AS data_hora,
            cl.NomeCli AS clinica,
            cl.Telefone AS telefone_clinica,
            m.NomeMed AS medico,
            m.Especialidade AS especialidade,
            p.NomePac AS paciente,
            p.Telefone AS telefone_paciente,
            p.Email AS email_paciente,
            DATEDIFF(c.Data_Hora, NOW()) AS dias_ate_consulta,
            HOUR(c.Data_Hora) AS hora_consulta
        FROM Consulta c
        INNER JOIN Clinica cl ON c.CodCli = cl.CodCli
        INNER JOIN Medico m ON c.CodMed = m.CodMed
        INNER JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        WHERE c.Data_Hora BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL %s DAY)
        ORDER BY c.Data_Hora
        """
        rows = self._execute(sql, params=(dias,), fetchall=True)
        return rows or []

    def get_resumo_geral_sistema(self):
        """
        Dashboard completo com estatísticas gerais do sistema.
        Usa: múltiplas agregações e subconsultas
        """
        sql = """
        SELECT
            (SELECT COUNT(*) FROM Paciente) AS total_pacientes,
            (SELECT COUNT(*) FROM Medico) AS total_medicos,
            (SELECT COUNT(*) FROM Clinica) AS total_clinicas,
            (SELECT COUNT(*) FROM Consulta) AS total_consultas,
            (SELECT COUNT(*) FROM Consulta WHERE Data_Hora >= CURDATE()) AS consultas_futuras,
            (SELECT COUNT(*) FROM Consulta WHERE Data_Hora < NOW()) AS consultas_passadas,
            (SELECT COUNT(DISTINCT Especialidade) FROM Medico WHERE Especialidade != '') AS especialidades_disponiveis,
            (SELECT ROUND(AVG(YEAR(CURDATE()) - YEAR(DataNascimento)), 1) FROM Paciente) AS idade_media_pacientes
        """
        row = self._execute(sql, fetchone=True)
        return row or {}

    def get_historico_paciente(self, cpf: str):
        """
        Histórico completo de consultas de um paciente.
        Usa: múltiplos JOINs, ORDER BY com data
        """
        self.validate_cpf(cpf)
        sql = """
        SELECT
            c.Data_Hora AS data_hora,
            cl.NomeCli AS clinica,
            cl.Endereco AS endereco_clinica,
            cl.Telefone AS telefone_clinica,
            m.NomeMed AS medico,
            m.Especialidade AS especialidade,
            m.Telefone AS telefone_medico,
            CASE
                WHEN c.Data_Hora < NOW() THEN 'Realizada'
                ELSE 'Agendada'
            END AS status
        FROM Consulta c
        INNER JOIN Clinica cl ON c.CodCli = cl.CodCli
        INNER JOIN Medico m ON c.CodMed = m.CodMed
        WHERE c.CpfPaciente = %s
        ORDER BY c.Data_Hora DESC
        """
        rows = self._execute(sql, params=(cpf,), fetchall=True)
        return rows or []

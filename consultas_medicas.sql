BEGIN;

DROP SCHEMA IF EXISTS consultas_medicas;
CREATE SCHEMA consultas_medicas;
USE consultas_medicas;

-- CRIANDO AS TABELAS
CREATE TABLE Clinica (
	CodCli CHAR(7) NOT NULL PRIMARY KEY,
    NomeCli VARCHAR(20) NOT NULL,
    Endereco VARCHAR(50) NOT NULL,
    Telefone CHAR(14) NOT NULL,
    Email VARCHAR(40) NOT NULL
);

CREATE TABLE Medico (
	CodMed CHAR(7) NOT NULL PRIMARY KEY,
    NomeMed VARCHAR(60) NOT NULL, 
    Genero CHAR(1) NOT NULL,
    Telefone CHAR(15) NOT NULL,
    Email VARCHAR(40) NOT NULL,
    Especialidade VARCHAR(30) NOT NULL
);

CREATE TABLE Paciente(
	CpfPaciente CHAR(14) NOT NULL PRIMARY KEY,
    NomePac VARCHAR(60) NOT NULL,
    DataNascimento DATE NOT NULL,
    Genero CHAR(1) NOT NULL,
    Telefone CHAR(15) NOT NULL,
    Email VARCHAR(40) NOT NULL
);

CREATE TABLE Consulta (
	CodCli CHAR(7) NOT NULL,
	CodMed CHAR(7) NOT NULL,
	CpfPaciente CHAR(14) NOT NULL,
	Data_Hora DATETIME NOT NULL,
	PRIMARY KEY (CodCli, CodMed, CpfPaciente, Data_Hora),
	FOREIGN KEY (CodCli) REFERENCES Clinica (CodCli) ON DELETE CASCADE,
	FOREIGN KEY (CodMed) REFERENCES Medico (CodMed),
	FOREIGN KEY (CpfPaciente) REFERENCES Paciente (CpfPaciente)
);

-- POPULANDO O BANCO
INSERT INTO Clinica VALUES
('0000001', 'Saúde Plus', 'Av. Rosa e Silva, 406, Graças', '(81) 4002-3633', 'saudeplus@mail.com'),
('0000002', 'Visão Recife', 'Av. Governador Agamenon Magalhães, 810', '(81) 3042-1112', 'visaorecife@mail.com'),
('0000003', 'Bem Viver', 'Rua da Aurora, 1250, Santo Amaro', '(81) 3221-8899', 'bemviver@mail.com'),
('0000004', 'OrtoLine', 'Rua Padre Carapuceiro, 620, Boa Viagem', '(81) 3093-4411', 'ortoline@mail.com'),
('0000005', 'Clínica Vida Plena', 'Av. Norte Miguel Arraes, 3450, Casa Amarela', '(81) 3445-7766', 'vidaplena@mail.com'),
('0000006', 'RecifeLab', 'Rua Dom Bosco, 55, Boa Vista', '(81) 3231-9922', 'recifelab@mail.com'),
('0000007', 'CardioCenter', 'Av. Domingos Ferreira, 2820, Boa Viagem', '(81) 3466-2077', 'cardiocenter@mail.com'),
('0000008', 'OdontoMaster', 'Rua do Futuro, 250, Aflitos', '(81) 3267-5500', 'odontomaster@mail.com'),
('0000009', 'Dermaclin', 'Av. Rui Barbosa, 987, Graças', '(81) 3125-7711', 'dermaclin@mail.com'),
('0000010', 'OrtoRecife', 'Rua Setúbal, 1440, Boa Viagem', '(81) 3099-1040', 'ortorecife@mail.com');

INSERT INTO Medico VALUES
('2819374', 'Marcela Gomes', 'F', '(81) 98273-3245', 'marcelagomes@mail.com', 'Pediatria'),
('5793149', 'Fernanda Vieira', 'F', '(81) 99240-2571', 'fernandavieira@mail.com', 'Pediatria'),
('8532974', 'Lucas Carvalho', 'M', '(81) 98256-5703', 'lucascarvalho@mail.com', 'Oftalmologia'),
('9183424', 'Fernanda Alencar', 'M', '(81) 99482-4758', 'fernandoalencar@mail.com', 'Oftalmologia'),
('1029485', 'João Henrique', 'M', '(81) 98122-4478', 'joaohenrique@mail.com', 'Cardiologia'),
('4092718', 'Mariana Lopes', 'F', '(81) 98455-2033', 'marianalopes@mail.com', 'Dermatologia'),
('2049586', 'Ricardo Matos', 'M', '(81) 98710-8894', 'ricardomatos@mail.com', 'Ortopedia'),
('7281985', 'Ana Letícia', 'F', '(81) 99542-6612', 'analeticia@mail.com', 'Ginecologia'),
('3495823', 'Paulo Sérgio', 'M', '(81) 98340-4421', 'paulosergio@mail.com', 'Otorrinolaringologia'),
('1039586', 'Camila Freitas', 'F', '(81) 98612-5014', 'camilafreitas@mail.com', 'Psiquiatria'),
('1958432', 'Roberto Tavares', 'M', '(81) 98177-2098', 'robertotavares@mail.com', 'Neurologia'),
('2819382', 'Juliana Moura', 'F', '(81) 98403-5580', 'julianamoura@mail.com', 'Endocrinologia');

INSERT INTO Paciente VALUES
('345.123.897-65', 'Rebeca Lins', '1993-04-15', 'F', '(81) 99945-4177', 'rebeca@mail.com'),
('589.612.347-52', 'Paulo Martins', '2020-08-21', 'M', '(81) 99873-4312', 'paulo@mail.com'),
('764.239.187-54', 'Ana Beatriz Souza', '1988-11-03', 'F', '(81) 98721-4401', 'anabeatriz@mail.com'),
('912.345.678-22', 'Carlos Eduardo Lima', '1975-06-27', 'M', '(81) 99320-5587', 'carloseduardo@mail.com'),
('457.891.236-90', 'Marina Albuquerque', '2002-02-14', 'F', '(81) 98431-7762', 'marinaalbuquerque@mail.com'),
('623.987.451-20', 'Thiago Moura', '1999-09-09', 'M', '(81) 99104-3328', 'thiagomoura@mail.com'),
('804.512.369-77', 'Jéssica Paiva', '1985-12-30', 'F', '(81) 99980-4421', 'jessicapaiva@mail.com'),
('358.710.249-66', 'Rafael Gomes', '2010-03-19', 'M', '(81) 98850-1194', 'rafaelgomes@mail.com');

INSERT INTO Consulta VALUES
('0000001', '2819374', '589.612.347-52', '2025-11-03 15:00:00'),
('0000002', '8532974', '345.123.897-65', '2025-12-10 16:40:00'),
('0000002', '9183424', '345.123.897-65', '2025-12-10 10:30:00'),
('0000001', '5793149', '589.612.347-52', '2025-11-15 09:20:00'),
('0000002', '8532974', '457.891.236-90', '2025-12-18 14:10:00'),
('0000002', '9183424', '804.512.369-77', '2025-12-05 08:45:00'),
('0000007', '1029485', '912.345.678-22', '2025-10-22 11:00:00'),
('0000007', '1029485', '623.987.451-20', '2025-09-14 09:30:00'),
('0000009', '4092718', '764.239.187-54', '2025-11-20 13:40:00'),
('0000004', '2049586', '358.710.249-66', '2025-11-08 15:55:00'),
('0000005', '7281985', '804.512.369-77', '2025-10-30 10:15:00'),
('0000008', '3495823', '345.123.897-65', '2025-11-27 09:50:00'),
('0000008', '3495823', '457.891.236-90', '2025-12-02 14:30:00'),
('0000010', '1039586', '764.239.187-54', '2025-12-12 16:10:00'),
('0000006', '1958432', '912.345.678-22', '2025-11-29 08:20:00'),
('0000003', '2819382', '623.987.451-20', '2025-12-03 11:30:00');

-- VISUALIZACAO DE CONSULTAS POR MÉDICO
CREATE VIEW Vw_QtdeConsultasPorMedico AS
SELECT 
    m.CodMed,
    m.NomeMed,
    m.Especialidade,
    COUNT(c.CodMed) AS TotalConsultas
FROM Medico m
LEFT JOIN Consulta c ON m.CodMed = c.CodMed
GROUP BY m.CodMed, m.NomeMed, m.Especialidade;

-- TRIGGERS
-- VALIDAÇÃO DE CPF DO PACIENTE
DROP TRIGGER IF EXISTS trg_validar_cpf_paciente_ins;
DELIMITER $$
CREATE TRIGGER trg_validar_cpf_paciente_ins
BEFORE INSERT ON Paciente
FOR EACH ROW
BEGIN
    -- CPF deve estar exatamente no formato XXX.XXX.XXX-XX
    IF NEW.CpfPaciente NOT REGEXP '^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CPF inválido. Formato obrigatório: XXX.XXX.XXX-XX';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_validar_cpf_paciente_upd;
DELIMITER $$
CREATE TRIGGER trg_validar_cpf_paciente_upd
BEFORE UPDATE ON Paciente
FOR EACH ROW
BEGIN
    IF NEW.CpfPaciente NOT REGEXP '^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CPF inválido. Formato obrigatório: XXX.XXX.XXX-XX';
    END IF;
END$$
DELIMITER ;

-- VALIDAÇÃO DE E-MAIL DA CLINICA
DROP TRIGGER IF EXISTS trg_valida_email_clinica;
DELIMITER $$
CREATE TRIGGER trg_valida_email_clinica
BEFORE INSERT ON Clinica
FOR EACH ROW
BEGIN
    -- Verifica presença de @ e .
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail da clínica em formato inválido.';
    END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_valida_email_clinica_upd;
DELIMITER $$
CREATE TRIGGER trg_valida_email_clinica_upd
BEFORE UPDATE ON Clinica
FOR EACH ROW
BEGIN
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail da clínica em formato inválido.';
    END IF;
END $$
DELIMITER ;


-- VALIDAÇÃO DE E-MAIL DO PACIENTE
DROP TRIGGER IF EXISTS trg_valida_email_paciente;
DELIMITER $$
CREATE TRIGGER trg_valida_email_paciente
BEFORE INSERT ON Paciente
FOR EACH ROW
BEGIN
    -- Verifica presença de @ e .
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail do paciente em formato inválido.';
    END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_valida_email_paciente_upd;
DELIMITER $$
CREATE TRIGGER trg_valida_email_paciente_upd
BEFORE UPDATE ON Paciente
FOR EACH ROW
BEGIN
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail do paciente em formato inválido.';
    END IF;
END $$
DELIMITER ;

-- VALIDAÇÃO DE E-MAIL DO MÉDICO
DROP TRIGGER IF EXISTS trg_valida_email_medico;
DELIMITER $$
CREATE TRIGGER trg_valida_email_medico
BEFORE INSERT ON Medico
FOR EACH ROW
BEGIN
    -- Verifica presença de @ e .
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail do médico em formato inválido.';
    END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_valida_email_medico_upd;
DELIMITER $$
CREATE TRIGGER trg_valida_email_medico_upd
BEFORE UPDATE ON Medico
FOR EACH ROW
BEGIN
    IF NEW.Email NOT LIKE '%_@_%._%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'E-mail do médico em formato inválido.';
    END IF;
END $$
DELIMITER ;

-- VALIDAÇÃO DO TELEFONE DA CLÍNICA
DROP TRIGGER IF EXISTS trg_validar_telefone_clinica_ins;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_clinica_ins
BEFORE INSERT ON Clinica
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{4}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone da clínica inválido. Formato esperado: (DD) XXXX-XXXX';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_validar_telefone_clinica_upd;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_clinica_upd
BEFORE UPDATE ON Clinica
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{4}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone da clínica inválido. Formato esperado: (DD) XXXX-XXXX';
    END IF;
END$$
DELIMITER ;

-- VALIDAÇÃO DE TELEFONE DO MÉDICO
DROP TRIGGER IF EXISTS trg_validar_telefone_medico_ins;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_medico_ins
BEFORE INSERT ON Medico
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{5}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone do médico inválido. Formato esperado: (DD) XXXXX-XXXX';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_validar_telefone_medico_upd;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_medico_upd
BEFORE UPDATE ON Medico
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{5}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone do médico inválido. Formato esperado: (DD) XXXXX-XXXX';
    END IF;
END$$
DELIMITER ;

-- VALIDAÇÃO DO TELEFONE DO PACIENTE
DROP TRIGGER IF EXISTS trg_validar_telefone_paciente_ins;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_paciente_ins
BEFORE INSERT ON Paciente
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{5}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone do paciente inválido. Formato esperado: (DD) XXXXX-XXXX';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_validar_telefone_paciente_upd;
DELIMITER $$
CREATE TRIGGER trg_validar_telefone_paciente_upd
BEFORE UPDATE ON Paciente
FOR EACH ROW
BEGIN
    IF TRIM(NEW.Telefone) NOT RLIKE '^\\([0-9]{2}\\)[[:space:]]*[0-9]{5}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone do paciente inválido. Formato esperado: (DD) XXXXX-XXXX';
    END IF;
END$$
DELIMITER ;

COMMIT;

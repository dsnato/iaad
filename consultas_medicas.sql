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
('5793149', 'Amanda Vieira', 'F', '(81) 99240-2571', 'amandavieira@mail.com', 'Pediatria'),
('8532974', 'Lucas Carvalho', 'M', '(81) 98256-5703', 'lucascarvalho@mail.com', 'Oftalmologia'),
('9183424', 'Alexandre Alencar', 'M', '(81) 99482-4758', 'alexandrealencar@mail.com', 'Oftalmologia'),
('1029485', 'João Henrique', 'M', '(81) 98122-4478', 'joaohenrique@mail.com', 'Cardiologia'),
('4092718', 'Mariana Lopes', 'F', '(81) 98455-2033', 'marianalopes@mail.com', 'Dermatologia'),
('2049586', 'Ricardo Matos', 'M', '(81) 98710-8894', 'ricardomatos@mail.com', 'Ortopedia'),
('7281985', 'Ana Letícia', 'F', '(81) 99542-6612', 'analeticia@mail.com', 'Ginecologia'),
('3495823', 'Paulo Sérgio', 'M', '(81) 98340-4421', 'paulosergio@mail.com', 'Otorrinolaringologia'),
('1039586', 'Camila Freitas', 'F', '(81) 98612-5014', 'camilafreitas@mail.com', 'Psiquiatria'),
('1958432', 'Roberto Tavares', 'M', '(81) 98177-2098', 'robertotavares@mail.com', 'Neurologia'),
('2819382', 'Juliana Moura', 'F', '(81) 98403-5580', 'julianamoura@mail.com', 'Endocrinologia'),
('6748291', 'Carlos Alberto', 'M', '(81) 98765-4321', 'carlosalberto@mail.com', 'Cardiologia'),
('3829174', 'Bruno Oliveira', 'M', '(81) 99876-5432', 'brunooliveira@mail.com', 'Neurologia'),
('9182736', 'Carolina Santos', 'F', '(81) 98654-3210', 'carolinasantos@mail.com', 'Pediatria'),
('4728193', 'Daniel Ferreira', 'M', '(81) 99765-4321', 'danielferreira@mail.com', 'Ortopedia'),
('8372619', 'Elena Rodrigues', 'F', '(81) 98543-2109', 'elenarodrigues@mail.com', 'Ginecologia'),
('2918374', 'Felipe Mendes', 'M', '(81) 99654-3210', 'felipemendes@mail.com', 'Dermatologia'),
('7382910', 'Gabriela Lima', 'F', '(81) 98432-1098', 'gabrielalima@mail.com', 'Oftalmologia'),
('1827364', 'Henrique Souza', 'M', '(81) 99543-2109', 'henriquesouza@mail.com', 'Gastroenterologia'),
('6291837', 'Isabela Nunes', 'F', '(81) 98321-0987', 'isabelanunes@mail.com', 'Pneumologia'),
('3719284', 'Leonardo Costa', 'M', '(81) 99432-1098', 'leonardocosta@mail.com', 'Urologia');

INSERT INTO Paciente VALUES
('345.123.897-65', 'Rebeca Lins', '1993-04-15', 'F', '(81) 99945-4177', 'rebeca@mail.com'),
('589.612.347-52', 'Paulo Martins', '2020-08-21', 'M', '(81) 99873-4312', 'paulo@mail.com'),
('764.239.187-54', 'Ana Beatriz Souza', '1988-11-03', 'F', '(81) 98721-4401', 'anabeatriz@mail.com'),
('912.345.678-22', 'Carlos Eduardo Lima', '1975-06-27', 'M', '(81) 99320-5587', 'carloseduardo@mail.com'),
('457.891.236-90', 'Marina Albuquerque', '2002-02-14', 'F', '(81) 98431-7762', 'marinaalbuquerque@mail.com'),
('623.987.451-20', 'Thiago Moura', '1999-09-09', 'M', '(81) 99104-3328', 'thiagomoura@mail.com'),
('804.512.369-77', 'Jéssica Paiva', '1985-12-30', 'F', '(81) 99980-4421', 'jessicapaiva@mail.com'),
('358.710.249-66', 'Rafael Gomes', '2010-03-19', 'M', '(81) 98850-1194', 'rafaelgomes@mail.com'),
('123.456.789-10', 'Fernanda Costa', '1990-07-22', 'F', '(81) 98877-6543', 'fernandacosta@mail.com'),
('234.567.890-12', 'Gustavo Mendes', '1982-03-14', 'M', '(81) 99765-4320', 'gustavomendes@mail.com'),
('345.678.901-23', 'Juliana Ribeiro', '1995-11-08', 'F', '(81) 98654-3219', 'julianaribeiro@mail.com'),
('456.789.012-34', 'Marcos Vieira', '1978-09-30', 'M', '(81) 99543-2108', 'marcosvieira@mail.com'),
('567.890.123-45', 'Natália Ferreira', '2001-05-17', 'F', '(81) 98432-1097', 'nataliaferreira@mail.com'),
('678.901.234-56', 'Pedro Henrique', '2015-01-25', 'M', '(81) 99321-0986', 'pedrohenrique@mail.com'),
('789.012.345-67', 'Raquel Nunes', '1987-08-12', 'F', '(81) 98210-9875', 'raquelnunes@mail.com'),
('890.123.456-78', 'Sérgio Almeida', '1969-04-03', 'M', '(81) 99109-8764', 'sergioalmeida@mail.com'),
('901.234.567-89', 'Tatiana Lopes', '1998-12-19', 'F', '(81) 98098-7653', 'tatianarlopes@mail.com'),
('012.345.678-90', 'Vinicius Santos', '2008-06-07', 'M', '(81) 99987-6542', 'viniciussantos@mail.com'),
('147.258.369-01', 'Amanda Silva', '1991-02-28', 'F', '(81) 98876-5431', 'amandasilva@mail.com'),
('258.369.147-02', 'Bruno Carvalho', '1984-10-11', 'M', '(81) 99764-3209', 'brunocarvalho@mail.com');

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
('0000003', '2819382', '623.987.451-20', '2025-12-03 11:30:00'),
('0000002', '8532974', '345.123.897-65', '2026-01-05 10:30:00'),
('0000001', '2819374', '123.456.789-10', '2026-01-10 09:00:00'),
('0000002', '7382910', '234.567.890-12', '2026-01-12 14:30:00'),
('0000007', '6748291', '345.678.901-23', '2026-01-15 10:45:00'),
('0000004', '4728193', '456.789.012-34', '2026-01-18 16:00:00'),
('0000005', '8372619', '567.890.123-45', '2026-01-20 08:30:00'),
('0000001', '9182736', '678.901.234-56', '2026-01-22 11:15:00'),
('0000006', '3829174', '789.012.345-67', '2026-01-25 15:45:00'),
('0000009', '2918374', '890.123.456-78', '2026-01-28 09:30:00'),
('0000003', '1827364', '901.234.567-89', '2026-02-01 13:00:00'),
('0000008', '6291837', '012.345.678-90', '2026-02-05 10:00:00'),
('0000010', '3719284', '147.258.369-01', '2026-02-08 14:20:00'),
('0000007', '1029485', '258.369.147-02', '2026-02-10 09:45:00'),
('0000002', '9183424', '123.456.789-10', '2026-02-12 16:30:00'),
('0000001', '5793149', '234.567.890-12', '2026-02-15 08:15:00'),
('0000004', '2049586', '345.678.901-23', '2026-02-18 11:00:00'),
('0000005', '7281985', '456.789.012-34', '2026-02-20 14:45:00'),
('0000003', '2819382', '567.890.123-45', '2026-02-22 10:30:00'),
('0000006', '1958432', '678.901.234-56', '2026-02-25 15:00:00'),
('0000009', '4092718', '789.012.345-67', '2026-02-28 09:00:00'),
('0000008', '3495823', '890.123.456-78', '2026-03-02 13:30:00'),
('0000010', '1039586', '901.234.567-89', '2026-03-05 10:15:00'),
('0000007', '6748291', '012.345.678-90', '2026-03-08 14:00:00'),
('0000002', '8532974', '147.258.369-01', '2026-03-10 09:30:00'),
('0000001', '2819374', '258.369.147-02', '2026-03-12 16:00:00'),
('0000004', '4728193', '123.456.789-10', '2026-03-15 08:45:00'),
('0000005', '8372619', '234.567.890-12', '2026-03-18 11:30:00'),
('0000003', '1827364', '345.678.901-23', '2026-03-20 15:15:00'),
('0000006', '3829174', '456.789.012-34', '2026-03-22 10:00:00'),
('0000009', '2918374', '567.890.123-45', '2026-03-25 13:45:00'),
('0000008', '6291837', '678.901.234-56', '2026-03-28 09:15:00'),
('0000010', '3719284', '789.012.345-67', '2026-03-30 14:30:00'),
('0000007', '9182736', '890.123.456-78', '2026-04-02 10:45:00'),
('0000002', '7382910', '901.234.567-89', '2026-04-05 15:30:00'),
('0000001', '5793149', '012.345.678-90', '2026-04-08 08:00:00');

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

-- TRIGGER
DROP TRIGGER IF EXISTS trg_verifica_intervalo_agendamento;
DELIMITER $$ 
CREATE TRIGGER tg_verifica_intervalo_agendamento
BEFORE INSERT ON Consulta
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(DAY, CURDATE(), NEW.Data_Hora) > 60 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A consulta só pode ser agendada com no máximo 2 meses de antecedência.';
    END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_verifica_intervalo_agendamento_upd
DELIMITER $$
CREATE TRIGGER tg_verifica_intervalo_agendamento_upd
BEFORE UPDATE ON Consulta
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(DAY, CURDATE(), NEW.Data_Hora) > 60 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A consulta só pode ser agendada com no máximo 2 meses de antecedência.';
    END IF;
END $$
DELIMITER ;

COMMIT;

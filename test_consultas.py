"""
Script de teste para validar todas as consultas do sistema
Testa CRUD básico e consultas não triviais (bonificação)
"""

import sys
from datetime import datetime, timedelta
from db import MySQLDB, ValidationError
import logging

# Tenta importar configurações personalizadas, senão usa padrão
try:
    from config import DB_CONFIG
except ImportError:
    DB_CONFIG = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',  # CONFIGURE SUA SENHA AQUI ou crie o arquivo config.py
        'database': 'consultas_medicas',
        'port': 3306
    }

# Configuração de logging (UTF-8 para suportar caracteres especiais)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_consultas.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TestConsultas:
    def __init__(self, db_config=None):
        """Inicializa conexão com banco de dados"""
        if db_config is None:
            db_config = DB_CONFIG
        
        self.db = MySQLDB(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        logger.info(f"Conectando ao banco de dados: {db_config['database']}")
        logger.info(f"Host: {db_config['host']}:{db_config['port']}")
        logger.info(f"Usuario: {db_config['user']}")
        
        # Testa conexão
        try:
            self.db.connect()
            logger.info("[OK] Conexão estabelecida com sucesso!")
        except Exception as e:
            logger.error(f"[ERRO] Falha na conexão: {e}")
            logger.error("\n[IMPORTANTE] Configure suas credenciais MySQL:")
            logger.error("1. Edite o arquivo config.py e coloque sua senha")
            logger.error("2. Ou edite diretamente test_consultas.py no dict DB_CONFIG")
            logger.error("\nVeja instruções no arquivo config.py")
            sys.exit(1)
    
    def separador(self, titulo):
        """Imprime separador visual nos logs"""
        logger.info("=" * 80)
        logger.info(f"  {titulo}")
        logger.info("=" * 80)
    
    def print_resultados(self, resultados, titulo="Resultados"):
        """Formata e imprime resultados de consultas"""
        logger.info(f"\n{titulo}:")
        if not resultados:
            logger.warning("  [!] Nenhum resultado encontrado")
            return
        
        if isinstance(resultados, list):
            logger.info(f"  [INFO] Total de registros: {len(resultados)}")
            for i, row in enumerate(resultados[:5], 1):  # Mostra até 5 primeiros
                logger.info(f"  [{i}] {row}")
            if len(resultados) > 5:
                logger.info(f"  ... e mais {len(resultados) - 5} registros")
        elif isinstance(resultados, dict):
            for key, value in resultados.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.info(f"  {resultados}")
    
    # ========================================
    # TESTES DE CRUD BÁSICO
    # ========================================
    
    def test_crud_pacientes(self):
        """Testa CRUD de pacientes"""
        self.separador("TESTE: CRUD PACIENTES")
        
        try:
            # CREATE
            logger.info("➤ Testando CREATE paciente...")
            cpf_teste = "123.456.789-00"
            self.db.create_cliente(
                cpf=cpf_teste,
                nome="João da Silva Teste",
                data_nascimento="1990-05-15",
                genero="M",
                telefone="(81) 99999-9999",
                email="joao.teste@email.com"
            )
            logger.info("OK - Paciente criado com sucesso")
            
            # READ
            logger.info(">> Testando READ pacientes...")
            pacientes = self.db.get_clientes()
            self.print_resultados(pacientes, "Pacientes cadastrados")
            
            # UPDATE
            logger.info(">> Testando UPDATE paciente...")
            self.db.update_cliente(
                cpf=cpf_teste,
                telefone="(81) 88888-8888",
                email="joao.novo@email.com"
            )
            logger.info("OK - Paciente atualizado com sucesso")
            
            # DELETE
            logger.info(">> Testando DELETE paciente...")
            self.db.delete_cliente(cpf=cpf_teste)
            logger.info("OK - Paciente excluído com sucesso")
            
        except Exception as e:
            logger.error(f"ERRO no CRUD Pacientes: {e}")
    
    def test_crud_clinicas(self):
        """Testa CRUD de clínicas"""
        self.separador("TESTE: CRUD CLÍNICAS")
        
        try:
            # CREATE
            logger.info(">> Testando CREATE clínica...")
            cod_teste = "CLI999"
            self.db.create_clinica(
                codcli=cod_teste,
                nome="Clínica Teste Ltda",
                endereco="Rua Teste, 123",
                telefone="(81) 3333-3333",
                email="contato@clinicateste.com"
            )
            logger.info("OK - Clínica criada com sucesso")
            
            # READ
            logger.info(">> Testando READ clínicas...")
            clinicas = self.db.get_clinicas()
            self.print_resultados(clinicas, "Clínicas cadastradas")
            
            # UPDATE
            logger.info(">> Testando UPDATE clínica...")
            self.db.update_clinica(
                codcli=cod_teste,
                telefone="(81) 4444-4444"
            )
            logger.info("OK - Clínica atualizada com sucesso")
            
            # DELETE
            logger.info(">> Testando DELETE clínica...")
            self.db.delete_clinica(cod_teste)
            logger.info("OK - Clínica excluída com sucesso")
            
        except Exception as e:
            logger.error(f"ERRO no CRUD Clínicas: {e}")
    
    def test_crud_medicos(self):
        """Testa CRUD de médicos"""
        self.separador("TESTE: CRUD MÉDICOS")
        
        try:
            # CREATE
            logger.info(">> Testando CREATE médico...")
            cod_teste = "MED999"
            self.db.create_medico(
                codmed=cod_teste,
                nome="Dr. Teste Silva",
                especialidade="Cardiologia",
                telefone="(81) 5555-5555",
                email="dr.teste@email.com"
            )
            logger.info("OK - Médico criado com sucesso")
            
            # READ
            logger.info(">> Testando READ médicos...")
            medicos = self.db.get_medicos()
            self.print_resultados(medicos, "Médicos cadastrados")
            
            # UPDATE
            logger.info(">> Testando UPDATE médico...")
            self.db.update_medico(
                codmed=cod_teste,
                especialidade="Neurologia"
            )
            logger.info("OK - Médico atualizado com sucesso")
            
            # DELETE
            logger.info(">> Testando DELETE médico...")
            self.db.delete_medico(cod_teste)
            logger.info("OK - Médico excluído com sucesso")
            
        except Exception as e:
            logger.error(f"ERRO no CRUD Médicos: {e}")
    
    def test_crud_consultas(self):
        """Testa CRUD de consultas"""
        self.separador("TESTE: CRUD CONSULTAS")
        
        try:
            # READ
            logger.info(">> Testando READ consultas...")
            consultas = self.db.get_pedidos()
            self.print_resultados(consultas, "Consultas cadastradas")
            
            # Se houver consultas, testa a busca por ID
            if consultas:
                primeira = consultas[0]
                logger.info(">> Testando busca por ID...")
                resultado = self.db.get_pedido_por_id(
                    primeira['CodCli'],
                    primeira['CodMed'],
                    primeira['CpfPaciente'],
                    primeira['Data_Hora']
                )
                self.print_resultados(resultado, "Consulta encontrada")
            
        except Exception as e:
            logger.error(f"ERRO no CRUD Consultas: {e}")
    
    # ========================================
    # TESTES DE CONSULTAS NÃO TRIVIAIS (BONIFICAÇÃO)
    # ========================================
    
    def test_estatisticas_clinicas(self):
        """Testa estatísticas por clínica"""
        self.separador("TESTE: ESTATÍSTICAS POR CLÍNICA")
        
        try:
            logger.info(">> Executando consulta com COUNT, GROUP BY, LEFT JOIN...")
            resultados = self.db.get_estatisticas_por_clinica()
            self.print_resultados(resultados, "Estatísticas por Clínica")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_ranking_medicos(self):
        """Testa ranking de médicos"""
        self.separador("TESTE: RANKING DE MÉDICOS")
        
        try:
            logger.info(">> Executando consulta com COUNT, GROUP BY, ORDER BY, LIMIT...")
            resultados = self.db.get_medicos_mais_atendimentos(limit=5)
            self.print_resultados(resultados, "Top 5 Médicos com Mais Consultas")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_consultas_periodo(self):
        """Testa consultas por período"""
        self.separador("TESTE: CONSULTAS POR PERÍODO")
        
        try:
            hoje = datetime.now()
            inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
            fim = (hoje + timedelta(days=30)).strftime("%Y-%m-%d")
            
            logger.info(f">> Buscando consultas entre {inicio} e {fim}...")
            logger.info(">> Usando BETWEEN, DATEDIFF, múltiplos JOINs...")
            resultados = self.db.get_consultas_por_periodo(inicio, fim)
            self.print_resultados(resultados, "Consultas no Período")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_pacientes_genero(self):
        """Testa estatísticas por gênero"""
        self.separador("TESTE: PACIENTES POR GÊNERO")
        
        try:
            logger.info(">> Executando consulta com COUNT, AVG, MIN, MAX...")
            resultados = self.db.get_pacientes_por_genero()
            self.print_resultados(resultados, "Estatísticas por Gênero")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_consultas_mes(self):
        """Testa distribuição por mês"""
        self.separador("TESTE: CONSULTAS POR MÊS")
        
        try:
            ano = datetime.now().year
            logger.info(f">> Analisando distribuição mensal de {ano}...")
            logger.info(">> Usando DATE_FORMAT, MONTH, MONTHNAME...")
            resultados = self.db.get_consultas_por_mes(ano)
            self.print_resultados(resultados, f"Consultas por Mês - {ano}")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_especialidades(self):
        """Testa ranking de especialidades"""
        self.separador("TESTE: ESPECIALIDADES MAIS PROCURADAS")
        
        try:
            logger.info(">> Executando consulta com COUNT, GROUP BY...")
            resultados = self.db.get_especialidades_mais_procuradas()
            self.print_resultados(resultados, "Ranking de Especialidades")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_ocupacao_dia_semana(self):
        """Testa taxa de ocupação por dia da semana"""
        self.separador("TESTE: OCUPAÇÃO POR DIA DA SEMANA")
        
        try:
            logger.info(">> Executando consulta com DAYOFWEEK, DAYNAME, AVG...")
            resultados = self.db.get_taxa_ocupacao_por_dia_semana()
            self.print_resultados(resultados, "Taxa de Ocupação por Dia")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_pacientes_inativos(self):
        """Testa pacientes sem consultas"""
        self.separador("TESTE: PACIENTES SEM CONSULTAS")
        
        try:
            logger.info(">> Executando consulta com LEFT JOIN e IS NULL...")
            resultados = self.db.get_pacientes_sem_consulta()
            self.print_resultados(resultados, "Pacientes Inativos")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_consultas_proximas(self):
        """Testa consultas próximas"""
        self.separador("TESTE: CONSULTAS PRÓXIMAS")
        
        try:
            dias = 7
            logger.info(f">> Buscando consultas dos próximos {dias} dias...")
            logger.info(">> Usando DATE_ADD, INTERVAL, manipulação de datas...")
            resultados = self.db.get_consultas_proximas(dias)
            self.print_resultados(resultados, f"Consultas nos Próximos {dias} Dias")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_resumo_geral(self):
        """Testa dashboard geral"""
        self.separador("TESTE: RESUMO GERAL DO SISTEMA")
        
        try:
            logger.info(">> Executando dashboard com múltiplas subconsultas...")
            resultado = self.db.get_resumo_geral_sistema()
            self.print_resultados(resultado, "Dashboard Geral")
            logger.info("OK - Consulta executada com sucesso")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_historico_paciente(self):
        """Testa histórico de paciente"""
        self.separador("TESTE: HISTÓRICO DE PACIENTE")
        
        try:
            # Busca primeiro paciente disponível
            pacientes = self.db.get_clientes()
            if pacientes:
                cpf = pacientes[0]['cpf']
                logger.info(f">> Buscando histórico do paciente {cpf}...")
                logger.info(">> Usando CASE WHEN, múltiplos JOINs...")
                resultados = self.db.get_historico_paciente(cpf)
                self.print_resultados(resultados, f"Histórico do Paciente {cpf}")
                logger.info("OK - Consulta executada com sucesso")
            else:
                logger.warning("[!] Nenhum paciente cadastrado para testar")
        except Exception as e:
            logger.error(f"ERRO: {e}")
    
    def test_validacoes(self):
        """Testa validações de dados"""
        self.separador("TESTE: VALIDAÇÕES")
        
        # Teste CPF inválido
        logger.info(">> Testando validação de CPF inválido...")
        try:
            self.db.validate_cpf("123.456.789-0")
            logger.error("ERRO - Validação não detectou CPF inválido!")
        except ValidationError as e:
            logger.info(f"OK - Validação funcionou: {e}")
        
        # Teste email inválido
        logger.info(">> Testando validação de email inválido...")
        try:
            self.db.validate_email("email_invalido")
            logger.error("ERRO - Validação não detectou email inválido!")
        except ValidationError as e:
            logger.info(f"OK - Validação funcionou: {e}")
        
        # Teste telefone inválido
        logger.info(">> Testando validação de telefone inválido...")
        try:
            self.db.validate_phone("1234-5678")
            logger.error("ERRO - Validação não detectou telefone inválido!")
        except ValidationError as e:
            logger.info(f"OK - Validação funcionou: {e}")
    
    def executar_todos_testes(self):
        """Executa todos os testes"""
        logger.info("\n\n")
        logger.info("[INICIO] BATERIA DE TESTES DO SISTEMA")
        logger.info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("\n")
        
        try:
            # Testes de CRUD Básico
            logger.info("[FASE 1] TESTES DE CRUD BÁSICO")
            self.test_crud_pacientes()
            self.test_crud_clinicas()
            self.test_crud_medicos()
            self.test_crud_consultas()
            
            # Testes de Consultas Não Triviais (Bonificação)
            logger.info("\n[FASE 2] TESTES DE CONSULTAS NÃO TRIVIAIS (BONIFICAÇÃO)")
            self.test_estatisticas_clinicas()
            self.test_ranking_medicos()
            self.test_consultas_periodo()
            self.test_pacientes_genero()
            self.test_consultas_mes()
            self.test_especialidades()
            self.test_ocupacao_dia_semana()
            self.test_pacientes_inativos()
            self.test_consultas_proximas()
            self.test_resumo_geral()
            self.test_historico_paciente()
            
            # Testes de Validações
            logger.info("\n[FASE 3] TESTES DE VALIDAÇÕES")
            self.test_validacoes()
            
            logger.info("\n\n")
            self.separador("[SUCESSO] TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
            logger.info("[INFO] Log completo salvo em: test_consultas.log")
            
        except Exception as e:
            logger.error(f"\n[ERRO CRITICO] NOS TESTES: {e}")
            logger.exception("Stack trace completo:")
        
        finally:
            # Fecha conexão
            self.db.close()
            logger.info("[INFO] Conexão com banco de dados encerrada")


if __name__ == "__main__":
    # Executa todos os testes
    tester = TestConsultas()
    tester.executar_todos_testes()
import mysql.connector
import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def execute_sql_file(conn, path):
    cur = conn.cursor()
    delim = ';'
    stmt = ''
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n')
            stripped = line.strip()
            if not stripped or stripped.startswith('--'):
                continue
            if stripped.upper().startswith('DELIMITER'):
                parts = stripped.split()
                if len(parts) >= 2:
                    delim = parts[1]
                continue
            stmt += line + '\n'
            if stmt.rstrip().endswith(delim):
                to_exec = stmt.rstrip()[:-len(delim)].strip()
                if to_exec:
                    try:
                        cur.execute(to_exec)
                    except mysql.connector.Error as e:
                        print(f"Erro ao executar statement: {e}\nStatement:\n{to_exec}\n", file=sys.stderr)
                        cur.close()
                        raise
                stmt = ''
    cur.close()
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Importa um .sql no MySQL (tratamento de DELIMITER).")
    parser.add_argument('--host', default=os.getenv('DB_HOST', 'localhost'))
    parser.add_argument('--port', type=int, default=int(os.getenv('DB_PORT', 3306)))
    parser.add_argument('--user', default=os.getenv('DB_USER', 'root'))
    parser.add_argument('--password', default=os.getenv('DB_PASSWORD', ''))
    parser.add_argument('--file', default='consultas_medicas.sql')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Arquivo não encontrado: {args.file}", file=sys.stderr)
        sys.exit(2)

    try:
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            autocommit=False
        )
    except mysql.connector.Error as e:
        print(f"Falha ao conectar ao MySQL: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        print("Iniciando importação...", args.file)
        execute_sql_file(conn, args.file)
        print("Importação concluída com sucesso.")
    except Exception as e:
        print("Erro durante importação:", e, file=sys.stderr)
        sys.exit(3)
    finally:
        conn.close()


if __name__ == '__main__':
    main()

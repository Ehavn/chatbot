import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresDB:
    def __init__(self, host, port, database, user, password, debug=False):
        self.debug = debug
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        if self.debug:
            print("✅ Conectado ao banco PostgreSQL")

    def insert_message(self, from_number, message_text, response_text):
        """Insere uma conversa no banco"""
        try:
            sql = """
                INSERT INTO conversas (from_number, message_text, response_text)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(sql, (from_number, message_text, response_text))
            if self.debug:
                print(f"💾 Mensagem gravada no banco: {from_number} -> {message_text}")
        except Exception as e:
            print("❌ Erro ao gravar no banco:", e)

    def close(self):
        self.cursor.close()
        self.conn.close()
        if self.debug:
            print("🔒 Conexão com o banco fechada")

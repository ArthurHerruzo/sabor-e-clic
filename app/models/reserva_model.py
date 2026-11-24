
from app.database import get_db


class ReservaModel:

    @staticmethod
    def listar_mesas_disponiveis(inicio, fim, quantidade_pessoas):
        db = get_db()

        return db.execute("""
            SELECT id_mesa, numero_mesa, capacidade
            FROM mesas
            WHERE capacidade >= ?
            AND id_mesa NOT IN (
                SELECT id_mesa
                FROM reservas
                WHERE status = 'ATIVA'
                AND data_hora_inicio < ?
                AND data_hora_fim > ?
            )
            ORDER BY numero_mesa
        """, (quantidade_pessoas, fim, inicio)).fetchall()

    @staticmethod
    def criar_reserva(id_usuario, id_mesa, quantidade_pessoas, inicio, fim):
        db = get_db()

        try:
            mesa = db.execute("""
                SELECT capacidade
                FROM mesas
                WHERE id_mesa = ?
            """, (id_mesa,)).fetchone()

            if not mesa or quantidade_pessoas > mesa['capacidade']:
                return False

            conflito = db.execute("""
                SELECT id_reserva
                FROM reservas
                WHERE id_mesa = ?
                AND status = 'ATIVA'
                AND data_hora_inicio < ?
                AND data_hora_fim > ?
            """, (id_mesa, fim, inicio)).fetchone()

            if conflito:
                return False

            db.execute("""
                INSERT INTO reservas (
                    id_usuario,
                    id_mesa,
                    quantidade_pessoas,
                    data_hora_inicio,
                    data_hora_fim
                )
                VALUES (?, ?, ?, ?, ?)
            """, (id_usuario, id_mesa, quantidade_pessoas, inicio, fim))

            db.commit()
            return True

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def listar_reservas():
        db = get_db()

        return db.execute("""
            SELECT
                r.id_reserva,
                r.id_usuario,
                u.nome AS nome_cliente,
                m.numero_mesa,
                m.capacidade,
                r.quantidade_pessoas,
                r.data_hora_inicio,
                r.data_hora_fim,
                r.status
            FROM reservas r
            INNER JOIN usuarios u
                ON r.id_usuario = u.id_usuario
            INNER JOIN mesas m
                ON r.id_mesa = m.id_mesa
            ORDER BY r.data_hora_inicio
        """).fetchall()
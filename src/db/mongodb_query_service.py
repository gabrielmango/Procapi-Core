from src.db.mongodb_connection import MongoDBConnection


class MongoDBQueryService:
    """Serviço para execução de consultas no MongoDB."""

    def __init__(self, logger, connection_string: str, db_name: str) -> None:
        self._logger = logger
        self._connection_string = connection_string
        self._db_name = db_name

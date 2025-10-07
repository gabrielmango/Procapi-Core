from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database


class MongoDBConnection:
    """Gerencia a conexão com um banco MongoDB."""

    def __init__(self, logger, connection_string: str, db_name: str) -> None:
        """Inicializa a classe MongoDBConnection."""
        self.connection_string = connection_string
        self.db_name: str = db_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self._logger = logger
        self._logger.logger.debug(f"SyncMongoDBConnection inicializado para db='{self.db_name}'")

    def __enter__(self) -> Database:
        """Abre a conexão com o MongoDB e retorna o objeto do banco."""
        try:
            self._logger.logger.debug(f"Tentando conectar ao MongoDB (sync), db='{self.db_name}'")
            self.client = MongoClient(self.connection_string)
            self._logger.logger.debug('Cliente MongoClient inicializado.')
            self.db = self.client[self.db_name]
            self._logger.logger.debug(f"Conexão estabelecida com o banco '{self.db_name}'")
            return self.db
        except Exception as e:
            self._logger.logger.error(f"Erro ao conectar ao MongoDB db='{self.db_name}': {str(e)}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão com o MongoDB ao sair do contexto."""
        if self.client:
            try:
                self._logger.logger.debug(f"Fechando conexão com o banco '{self.db_name}' (sync).")
                self.client.close()
                self._logger.logger.debug(f"Conexão com o banco '{self.db_name}' encerrada com sucesso")
            except Exception as e:
                self._logger.logger.error(f"Erro ao fechar conexão com MongoDB db='{self.db_name}': {str(e)}")

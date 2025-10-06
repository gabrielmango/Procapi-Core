from typing import Any, Dict, Optional

from bson import DBRef, ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongodb_connection import AsyncMongoDBConnection


class MongoDBQueryService:
    """Serviço genérico para execução de consultas no MongoDB."""

    def __init__(self, logger, connection_string: str, db_name: str) -> None:
        self._logger = logger
        self._connection_string = connection_string
        self._db_name = db_name

    async def find(self, collection_name, filter_query):
        self._logger.logger.debug(
            f"Busca '{collection_name}' com filtro: {filter_query}"
        )

        try:
            async with AsyncMongoDBConnection(
                self._logger, self._connection_string, self._db_name
            ) as db:
                collection = db[collection_name]
                document = await collection.find(filter_query)
                self._logger.logger.debug(f'Documento encontrado: {document}')
                return list(document)
        except Exception as e:
            self._logger.logger.error(f"Erro '{collection_name}': {e}")
        return None

    async def collection_exists(self, db, collection_name) -> bool:
        """Verifica se uma collection existe no banco de dados."""
        try:
            collections = await db.list_collection_names()
            exists = collection_name in collections
            self._logger.logger.debug(f"Existe '{collection_name}': {exists}")
            return exists
        except Exception as e:
            self._logger.logger.error(f"Erro '{collection_name}': {e}")
            return False

    async def find_ref(self, chave: str, id: str) -> Optional[Dict[str, Any]]:
        """Consulta um documento por referência (DBRef)."""
        self._logger.logger.debug(
            f"Iniciando find_ref: campo='{chave}', id='{id}'"
        )

        try:
            async with AsyncMongoDBConnection(
                self._logger, self._connection_string, self._db_name
            ) as db:
                collection = db[self._collection_name]
                filter_query = {chave: DBRef(chave, ObjectId(id))}
                document = await collection.find(filter_query)
                documents = list(document)
                self._logger.logger.debug(
                    f'Documentos encontrado via DBRef: {len(documents)}'
                )
                return documents
        except Exception as e:
            self._logger.logger.error(f'Erro ao executar find_ref: {e}')
        return None

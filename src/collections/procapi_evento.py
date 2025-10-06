from src.db.mongodb_query_service import MongoDBQueryService
from src.utils.load_env import LoadEnv
from src.utils.logger_manager import LoggerManager


class EventoPorProcesso:
    def __init__(self, ambiente):
        """Inicializa a classe."""
        self._ambiente = ambiente.upper()
        self._db_name = 'dbprocapi'
        self._logger = LoggerManager('eventos_por_processo')
        self._acesso_procapi = LoadEnv(
            [
                'PROCAPI_PROD',
                'PROCAPI_PREPROD',
                'PROCAPI_HML',
                'PROCAPI_TST',
                'PROCAPI_DEV',
            ]
        ).get_variables()

        connection_string = self._acesso_procapi.get(
            f'PROCAPI_{self._ambiente}'
        )

        self._mongodb_query = MongoDBQueryService(
            logger=self._logger,
            connection_string=connection_string,
            db_name=self._db_name,
        )

        self._eventos = None

    async def busca_eventos_por_processo(self, numero_processo: str) -> None:
        """Executa o fluxo de busca de eventos para um processo específico."""

        @self._logger.log_execution
        async def run():
            await self.busca_eventos(numero_processo)

        await run()

        return self._eventos

    async def busca_eventos(self, numero_processo: str) -> None:
        """Busca os eventos relacionados a um processo específico."""

        self._logger.logger.debug(
            f'Iniciando busca de eventos para processo: {numero_processo}'
        )

        try:
            eventos = await self._mongodb_query.find_ref(
                chave='processo', id=numero_processo
            )

            self._logger.logger.info(
                f'Eventos encontrados para processo {numero_processo}: {len(eventos)}'
            )

            self._eventos = eventos

        except Exception as e:
            self._logger.logger.error(
                f'Erro ao buscar eventos para processo {numero_processo}: {e}'
            )

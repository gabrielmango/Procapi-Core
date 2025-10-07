from src.modulos.collection_aviso import CollectionAviso
from src.utils.logger_manager import LoggerManager

logger = LoggerManager('consulta_avisos_por_processo')


@logger.log_execution
def main():
    processos = ['10002018920258130024']

    collection_aviso = CollectionAviso(logger=logger, ambiente='prod')

    for processo in processos:
        info = collection_aviso.consulta_avisos_por_processo(processo)
        logger.logger.info(f"Numero aviso: {info['numero']} - situacao: {info['situacao']}")


if __name__ == '__main__':
    main()

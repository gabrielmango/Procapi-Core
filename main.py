from src.utils.logger_manager import LoggerManager

logger = LoggerManager('example')


@logger.log_execution
def main():
    logger.logger.info('Running process...')


if __name__ == '__main__':
    main()

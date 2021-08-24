import logging

def append_logging_handler(handler, formatter, level):
    handler.setFormatter(logging.Formatter(formatter))
    handler.setLevel(level)
    logger = logging.getLogger('')
    if level < logger.level:
        logger.setLevel(level)
    logger.addHandler(handler)

def test():
    import sys
    
    append_logging_handler(
        logging.StreamHandler(sys.stdout),
        '[%(asctime)s %(levelname)s %(module)s %(funcName)s] %(message)s',
        logging.DEBUG)
    
    logging.info('info1')
    logging.debug('debug log')
    
    append_logging_handler(
        logging.FileHandler("my_log.log", mode='w'),
        '[%(asctime)s %(levelname)s %(module)s %(funcName)s] %(message)s',
        logging.INFO)
    
    logging.debug('debug log2')
    logging.warning('warning')
    logging.info('info1')
    logging.error('error')
    try:
        1/0
    except:
        logging.exception('exp')

def main():
    test()

if __name__ == '__main__':
    main()

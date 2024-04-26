import logging


def initialize_logging(level=logging.INFO, folder: str = '.'):
    '''
    initialize logging (default to file 'out.log' in folder and to stdout)
    '''
    logger_ = logging.getLogger('app')
    logger_.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler = logging.FileHandler(f'{folder}/out.log')
    filehandler.setLevel(level)
    filehandler.setFormatter(formatter)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(level)
    streamhandler.setFormatter(formatter)
    logger_.addHandler(filehandler)
    logger_.addHandler(streamhandler)
    return logger_

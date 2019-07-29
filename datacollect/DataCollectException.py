class Error(Exception):
    pass

class DataCollectError(Error):
    def __init__(self, error_type, error):
        self.__err_type = error_type
        self.__error = error
    def __str__(self):
        return 'query fail. errorType: {}, error: {}'.format(self.__err_type, self.__error)

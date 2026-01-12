class ReturnModel:
    def __init__(self, data, status = 200, exception = None, has_exception = False):
        self.data = data
        self.status = status
        self.exception = exception
        self.has_exception = has_exception
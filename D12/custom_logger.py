import logging


class CustomHandler(logging.Handler):
    def emit(self, record):
        print("I'm custom handler")
        pass

import logging


class HealthchechFilter(logging.Filter):
    def filter(self, record):
        return not record.args[0].startswith('GET /healthz')

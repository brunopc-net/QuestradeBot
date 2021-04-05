import log4p
import redis
import json

log = log4p.GetLogger(__name__).logger
redis = redis.Redis()


class TokenManager:

    @staticmethod
    def load(name):
        log.info("Loading token…")
        data = redis.get(name)
        if data is None:
            return data
        return json.loads(data)

    @staticmethod
    def store(name, token):
        log.info("Storing token…")
        data = json.dumps(token)
        redis.set(name, data)
        log.info("Storing token: done")

    @staticmethod
    def is_stored(name):
        return redis.exists(name)

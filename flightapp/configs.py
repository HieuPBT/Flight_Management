class Regulation:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.configuration = {}
            return cls.__instance
        else:
            return cls.__instance

    def get_regulation_value(self, key):
        return self.configuration.get(key)

    def set_regulation_value(self, key, value):
        self.configuration[key] = value
class ConfigurationSingleton:
    __instance = None  # Instance variable to store the Singleton instance

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.configuration = {}  # Load configuration from database
            # Load configuration from database here
            cls.__instance.load_configuration_from_database()
        return cls.__instance

    def load_configuration_from_database(self):
        # Replace this with your actual logic to load configuration from the database
        # For example, using SQLAlchemy
        # Assuming you have a QuyDinh model defined with key and value attributes
        from models import QuyDinh
        configurations = QuyDinh.query.all()
        for config in configurations:
            self.configuration[config.key] = config.value

    def get_configuration_value(self, key):
        return self.configuration.get(key)
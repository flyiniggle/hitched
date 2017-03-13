class ServerError(dict):
    def __init__(self, message):
        super(ServerError, self).__init__()
        self["error"] = str(message)
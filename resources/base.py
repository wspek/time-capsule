from reporting import Report


class Resource:
    type = ''

    def __init__(self, folder, connection_data, download_data):
        self.folder = folder
        self.connection_data = connection_data
        self.download_data = download_data
        self._report = Report(title=f'[{self.type}] Download Report')

    @classmethod
    def create(cls, type, **kwargs):
        subcls = next((klass for klass in cls.__subclasses__() if klass.type == type))
        return subcls(**kwargs)

    def connect(self):
        raise NotImplementedError

    def download(self):
        raise NotImplementedError

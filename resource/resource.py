from abc import ABC, abstractmethod

from reporting import Report


class Resource(ABC):
    type = ''

    def __init__(self, out_folder, connection_data, download_data):
        self.out_folder = out_folder
        self.connection_data = connection_data
        self.download_data = download_data
        self._report = Report(title=f'[{self.type}] Download Report')

    @abstractmethod
    def download_all(self):
        pass

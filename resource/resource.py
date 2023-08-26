from abc import ABC, abstractmethod


class Resource(ABC):
    type = ''

    def __init__(self, out_folder, connection_data, download_data, report):
        self.out_folder = out_folder
        self.connection_data = connection_data
        self.download_data = download_data
        self._report = report

    @abstractmethod
    def download_all(self):
        pass

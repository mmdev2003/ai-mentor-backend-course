import io
import gzip
import shutil

from weed import operation as op
from weed.util import WeedOperationResponse

from internal import interface


class Weed(interface.IStorage):
    def __init__(self, weed_master_host: str, weed_master_port: int):
        self.storage = op.WeedOperation("http://" + weed_master_host + ":" + str(weed_master_port))

    def delete(self, fid: str, name: str):
        return self.storage.crud_delete(fid=fid, file_name=name)

    def update(self, file: io.BytesIO, fid: str, name: str):
        return self.storage.crud_update(fp=file, fid=fid, file_name=name)

    def download(self, fid: str, name: str) -> tuple[io.BytesIO, str]:
        file_data = self.storage.crud_read(fid=fid, file_name=name)
        file = io.BytesIO(file_data.content)
        return file, file_data.content_type

    def upload(self, file: io.BytesIO, name: str) -> WeedOperationResponse:
        return self.storage.crud_create(fp=file, file_name=name)
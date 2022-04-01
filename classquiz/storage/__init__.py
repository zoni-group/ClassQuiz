from .deta_storage import DetaStorage
from .local_storage import LocalStorage
from io import BytesIO


class Storage:
    def __init__(self, backend: str, deta_key: str | None, deta_id: str | None, storage_path: str | None):
        self.backend = backend
        self.deta_key = deta_key
        self.deta_id = deta_id
        self.deta_base_url = f"https://drive.deta.sh/v1/{deta_id}/classquiz"
        self.deta_instance = DetaStorage(deta_base_url=self.deta_base_url, deta_key=self.deta_key, deta_id=self.deta_id)
        self.local_instance = LocalStorage(base_path=storage_path)
        if backend == "deta":
            if deta_key is None or deta_id is None:
                raise ValueError("deta_key and deta_id must be provided")
        if backend == "local":
            if storage_path is None:
                raise ValueError("storage_path must be provided")
        else:
            raise NotImplementedError(f"Backend {backend} not implemented")

    async def download(self, file_name: str) -> BytesIO | None:
        if self.backend == "deta":
            return await self.deta_instance.download(
                file_name)
        elif self.backend == "local":
            return await self.local_instance.get_file(file_name)

    async def upload(self, file_name: str, file_data: bytes) -> None:
        if self.backend == "deta":
            return await self.deta_instance.upload(file=file_data, file_name=file_name)
        elif self.backend == "local":
            return await self.local_instance.write_file(file_name=file_name, data=file_data)

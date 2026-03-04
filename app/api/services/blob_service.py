from azure.storage.blob import BlobServiceClient, ContentSettings
from app.api.core.config import settings
import uuid

client = BlobServiceClient(
    account_url=f"https://{settings.AZ_BLOB_ACCOUNT_NAME}.blob.core.windows.net",
    credential=settings.AZ_BLOB_ACCOUNT_KEY,
)


def upload_image(file_bytes: bytes) -> str:
    ext = file_bytes.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    blob = client.get_blob_client(
        container=settings.AZ_BLOB_CONTAINER_NAME, blob=filename
    )

    blob.upload_blob(
        file_bytes.file, content_settings=ContentSettings(content_type=f"image/{ext}")
    )

    return blob.url


def upload_file_path(filepath: str):
    ext = filepath.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    blob = client.get_blob_client(
        container=settings.AZ_BLOB_CONTAINER_NAME, blob=filename
    )

    with open(filepath, "rb") as file:
        blob.upload_blob(
            file, content_settings=ContentSettings(content_type=f"image/{ext}")
        )

    return blob.url

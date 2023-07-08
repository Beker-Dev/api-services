from app.core.config import settings
from minio import Minio
import os
from datetime import datetime, timedelta
import base64
from PIL import Image
import fastapi


class ImageExtensionNotAllowedException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


class MinioUtils:
    ADDRESS = settings.MINIO_ADDRESS
    ACCESS_KEY = settings.MINIO_ACCESS_KEY
    SECRET_KEY = settings.MINIO_SECRET_KEY
    SECURE_ACCESS = settings.MINIO_SECURE_ACCESS
    BUCKET_NAME = settings.MINIO_BUCKET_NAME if not settings.TESTING else 'testinginspectionsubstation'
    EXTENSIONS_ACCEPTED = settings.MINIO_EXTENSIONS_ACCEPTED

    @classmethod
    def get_minio_client(cls):
        client = Minio(cls.ADDRESS, cls.ACCESS_KEY, cls.SECRET_KEY, secure=cls.SECURE_ACCESS)
        if not client.bucket_exists(cls.BUCKET_NAME):
            client.make_bucket(cls.BUCKET_NAME)

        return client

    @classmethod
    def save_temp_file(cls, file):
        temp_dir = 'temp_files'
        _time = datetime.utcnow().strftime("%Y%m%d%H%S.%f")
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

        root_path = os.path.join(os.getcwd(), temp_dir)

        filename, file_ext = os.path.splitext(file.filename)
        cls.validate_file_extension(file_ext)
        new_filename = filename + _time + file_ext
        path = os.path.join(root_path, new_filename)

        Image.open(file.file).save(path)

        return new_filename, path, root_path

    @classmethod
    def remove_temp_file(cls, path):
        if os.path.isfile(path):
            os.remove(path)

    @classmethod
    def save_temp_file_thumbnail(cls, filename, file_path, root_path):
        thumb_filename = 'thumb_' + filename
        thumb_file_path = os.path.join(root_path, thumb_filename)

        img = Image.open(file_path)
        original_width, original_height = img.size
        new_width = 500
        new_height = 500

        if original_width <= new_width:
            img.save(thumb_file_path, optimize=True, quality=70)
        else:
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            img_resized.save(thumb_file_path, optimize=True, quality=70)
        return thumb_filename, thumb_file_path

    @classmethod
    def save_image(cls, img):
        client = cls.get_minio_client()

        filename, path, root_path = cls.save_temp_file(img)
        thumb_filename, thumb_file_path = cls.save_temp_file_thumbnail(filename, path, root_path)

        client.fput_object(
            bucket_name=cls.BUCKET_NAME,
            object_name=filename,
            file_path=path,
        )
        client.fput_object(
            bucket_name=cls.BUCKET_NAME,
            object_name=thumb_filename,
            file_path=thumb_file_path,
        )

        cls.remove_temp_file(path)
        cls.remove_temp_file(thumb_file_path)

        if settings.TESTING:
            cls.remove_bucket()

        return filename

    @classmethod
    def get_image(cls, img_name):
        client = cls.get_minio_client()
        return client.get_presigned_url('GET', cls.BUCKET_NAME, img_name, expires=timedelta(days=1))

    @classmethod
    def remove_image(cls, img_name):
        client = cls.get_minio_client()
        client.remove_object(cls.BUCKET_NAME, img_name)

    @classmethod
    def validate_file_extension(cls, extension):
        ext = extension[1:]
        if ext not in settings.MINIO_EXTENSIONS_ACCEPTED:
            raise ImageExtensionNotAllowedException(f'Extension {extension} not accepted')

    @classmethod
    def remove_bucket(cls):
        client = cls.get_minio_client()
        objects = client.list_objects(cls.BUCKET_NAME, recursive=True)
        for obj in objects:
            client.remove_object(cls.BUCKET_NAME, obj.object_name)
        else:
            client.remove_bucket(cls.BUCKET_NAME)

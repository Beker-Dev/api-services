from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_TITLE: str
    BACKEND_CORS_ORIGINS: List[str]
    ROOT_PATH: Optional[str] = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # DATABASE_URI: Optional[PostgresDsn] = None

    # MINIO_ADDRESS: str
    # MINIO_ACCESS_KEY: str
    # MINIO_SECRET_KEY: str
    # MINIO_SECURE_ACCESS: bool
    # MINIO_BUCKET_NAME: str
    # MINIO_EXTENSIONS_ACCEPTED: List[str]

    # KEYCLOAK_BASE_URL: str
    # KEYCLOAK_REALM: str
    # KEYCLOAK_CLIENT_ID: str
    # KEYCLOAK_CLIENT_SECRET: str

    # TESTING: Optional[bool] = False
    # TESTING_TOKEN: Optional[str]
    # IMAGE_FILE_TEST_PATH: Optional[str]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

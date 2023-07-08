# import jwt
# import requests
# from typing import Dict, Any
# from fastapi import Depends, HTTPException, Security, status
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from jwt.algorithms import RSAAlgorithm
# from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
#
# from app.core.config import settings
#
#
# REALM_PATH_KEYCLOAK = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
#
# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl=f"{REALM_PATH_KEYCLOAK}/protocol/openid-connect/auth",
#     tokenUrl=f"{REALM_PATH_KEYCLOAK}/protocol/openid-connect/token",
# )
#
#
# def get_public_key() -> _RSAPublicKey:
#     certs_url = f"{REALM_PATH_KEYCLOAK}/protocol/openid-connect/certs"
#     try:
#         response = requests.get(certs_url)
#         response.raise_for_status()
#         key_data = response.json()["keys"][1]
#         return RSAAlgorithm.from_jwk(key_data)
#     except requests.RequestException:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="Failed to retrieve public key for authentication.",
#         )
#
#
# def decode_jwt_token(token: str, public_key: RSAAlgorithm) -> Dict[str, Any]:
#     try:
#         options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
#         payload = jwt.decode(token, public_key, options=options, algorithms=["RS256"])
#         if not payload.get("sub"):
#             raise ValueError("Missing subject claim")
#         payload["access_token"] = token
#         return payload
#     except (jwt.PyJWTError, ValueError):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

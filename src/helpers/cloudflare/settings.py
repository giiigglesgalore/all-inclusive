import logging

logger = logging.getLogger(__name__)

try:
    from decouple import config
except ImportError:
    logger.info('python-decouple is not installed, using os.environ')
    import os

    config = os.environ.get


CLOUDFLARE_R2_CONFIG_OPTIONS = {}

#DJANGO STORAGES CONFIG
bucket_name=config("CLOUDFLARE_R2_BUCKET", cast=str)
access_key=config("CLOUDFLARE_R2_ACCESS_KEY", cast=str)
secret_key=config("CLOUDFLARE_R2_SECRET_KEY", cast=str)
endpoint_url=config("CLOUDFLARE_R2_BUCKET_ENDPOINT", cast=str)

if all([bucket_name, endpoint_url, access_key, secret_key]):
    CLOUDFLARE_R2_CONFIG_OPTIONS = {
        "bucket_name": bucket_name,
        "access_key": access_key,
        "secret_key": secret_key,
        "endpoint_url": endpoint_url,
        "default_acl": "public-read", # "private"
        "signature_version": "s3v4",
    }
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('127.0.0.1:9000',
                    access_key='minioadmin',
                    secret_key='minioadmin',
                    secure=False)

# Make a bucket with the make_bucket API call.
try:
    minioClient.make_bucket("maylogs", location="us-east-1")
except BucketAlreadyOwnedByYou as err:
    print(123)
except BucketAlreadyExists as err:
    print(1233)
except ResponseError as err:
    raise

# # Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
# try:
#     minioClient.fput_object('maylogs', 'pumaserver_debug.log', '/tmp/pumaserver_debug.log')
# except ResponseError as err:
#     print(err)

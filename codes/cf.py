import io, os

input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

os.write(1, b"123123")
input()

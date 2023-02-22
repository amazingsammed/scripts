# firstly pip install pysqlcipher3

import sqlite3
from sqlite3 import Error
from pysqlcipher3 import dbapi2 as sqlcipher

# Set up the encryption key
key = "mysecretpassword"

# Set up the source and destination filenames
src_file = "my_database.db"
dst_file = "my_encrypted_database.db"

# Open the unencrypted database
try:
    conn = sqlite3.connect(src_file)
except Error as e:
    print(e)

# Enable encryption with the key
conn.execute(f"PRAGMA key='{key}'")
conn.execute("PRAGMA cipher_compatibility=4")
conn.execute("PRAGMA kdf_iter=64000")
conn.execute("PRAGMA cipher_default_use_hmac=ON")

# Copy the unencrypted database to the encrypted file
with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
    fdst.write(fsrc.read())

# Open the encrypted database
enc_conn = sqlcipher.connect(dst_file)

# Enable encryption with the key
enc_conn.execute(f"PRAGMA key='{key}'")
enc_conn.execute("PRAGMA cipher_compatibility=4")
enc_conn.execute("PRAGMA kdf_iter=64000")
enc_conn.execute("PRAGMA cipher_default_use_hmac=ON")

# Close the database connections
conn.close()
enc_conn.close()
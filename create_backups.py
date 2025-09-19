import os
import tarfile
import random
import json
from datetime import datetime, timedelta

# --- Configuration ---
BACKUP_DIR = "backups"
NUM_DUMMY_BACKUPS = 100
FLAG_ID = 42
FLAG = "CTF{B4ckup_L3ak_f0r_th3_W1n!}"
# ---------------------

def create_dummy_content(file_path):
    """Creates some random-looking log data."""
    with open(file_path, "w") as f:
        lines = random.randint(50, 200)
        for i in range(lines):
            timestamp = (datetime.now() - timedelta(minutes=random.randint(1, 60*24*5))).isoformat()
            level = random.choice(["INFO", "WARN", "ERROR", "DEBUG"])
            message = random.choice([
                "User logged in successfully",
                "Failed password attempt",
                "Service started",
                "Database connection lost",
                "Cache cleared"
            ])
            f.write(f"{timestamp} [{level}] - Request ID {random.randint(1000,9999)}: {message}\n")

def create_tar_archive(tar_path, files_to_add):
    """Creates a .tar.gz archive from a list of files."""
    with tarfile.open(tar_path, "w:gz") as tar:
        for file_name, file_content_generator in files_to_add.items():
            # Create the temp file
            file_content_generator(file_name)
            # Add to tar
            tar.add(file_name)
            # Clean up the temp file
            os.remove(file_name)

def main():
    """Main function to generate all backup files."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    print(f"Generating {NUM_DUMMY_BACKUPS} dummy backup files...")

    for i in range(1, NUM_DUMMY_BACKUPS + 1):
        if i == FLAG_ID:
            continue # Skip the flag ID for now
        
        archive_name = os.path.join(BACKUP_DIR, f"backup{i}.tar.gz")
        files = {
            "app.log": create_dummy_content,
            "access.log": create_dummy_content
        }
        create_tar_archive(archive_name, files)

    # Now create the special backup with the flag
    print(f"Generating special backup with flag: backup{FLAG_ID}.tar.gz")
    
    # Create the secrets.json file content
    def create_secrets_file(file_path):
        secrets = {
            "db_password": "super_secret_password_123",
            "api_key": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
            "flag": FLAG
        }
        with open(file_path, 'w') as f:
            json.dump(secrets, f, indent=2)

    flag_archive_name = os.path.join(BACKUP_DIR, f"backup{FLAG_ID}.tar.gz")
    flag_files = {
        "app.log": create_dummy_content,
        "secrets.json": create_secrets_file
    }
    create_tar_archive(flag_archive_name, flag_files)
    
    print("\n✅ Done! Backup files created in the 'backups/' directory.")

if __name__ == "__main__":
    main()
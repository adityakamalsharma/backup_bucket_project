# CTF Challenge: IDOR + Backup Leak — Backup Bucket

This is a simple web challenge demonstrating an **Insecure Direct Object Reference (IDOR)** vulnerability that leads to a backup file leak.

## 🎯 Objective

The goal is to enumerate backup file IDs to find a hidden archive containing a `secrets.json` file. The flag is located inside this JSON file.

---

## 🚀 How to Build and Run

### Prerequisites
- [Docker](https://www.docker.com/get-started/) must be installed.

### Steps

1.  **Build the Docker Image:**
    Open your terminal in the project's root directory and run:
    ```bash
    docker build -t backup-bucket .
    ```

2.  **Run the Docker Container:**
    Run the image you just built, mapping the container's port 5000 to your local port 5000.
    ```bash
    docker run -p 5000:5000 backup-bucket
    ```
    The application will now be accessible at `http://localhost:5000`.

---

## 🕵️‍♂️ Player Instructions & How to Solve

1.  **Explore the Application:**
    Start by navigating to `http://localhost:5000`. You will see a backup server. The endpoint of interest is `/backups/<id>`, where `<id>` is a number.

2.  **Identify the Vulnerability:**
    Try accessing a few IDs manually, like `http://localhost:5000/backups/1`. You'll see that the server lets you download a file named `backup1.tar.gz`. This suggests you can access any backup if you can guess its ID (this is the IDOR).

3.  **Enumerate and Find the Secrets:**
    Since the IDs are simple integers, you can write a script (using `curl`, `wget`, or Python's `requests`) to loop through IDs (e.g., from 1 to 200) and check the server's response. A successful download (HTTP status 200) means a backup exists.
    
    Your goal is to find the one backup that is different—the one containing `secrets.json`.

4.  **Extract the Flag:**
    Once you have downloaded the correct `.tar.gz` archive (e.g., `backup42.tar.gz`), you need to extract its contents. You can use the `tar` command:
    ```bash
    # This command extracts the contents of the archive
    tar -xzvf backup42.tar.gz
    ```
    After extracting, you will see a `secrets.json` file. View its contents to find the flag!
    ```bash
    cat secrets.json
    ```
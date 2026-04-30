# 📂 Smart File Organizer

A Python-based automation tool that organizes files into structured folders and detects duplicates using hashing.

---

## 🚀 Features

- 📁 Automatic file categorization (Images, Videos, Documents, Audio, Others)
- 🔍 Duplicate file detection using hashing
- ⚡ Dry-run mode for safe testing (no actual changes)
- 📝 Logging system to track operations
- 📊 Progress display while processing files
- 🔄 Recursive directory handling

---

## 🧠 Tech Concepts Used

- Python OOP (Classes & Methods)
- File Handling (`os`, `shutil`)
- Exception Handling
- Hashing (MD5 for duplicate detection)
- Command-line arguments

---

## 📦 Project Structure

```
Smart_File_Organizer/
│
├── organizer.py
├── duplicate_finder.py
├── config.py
├── logger.py
├── main.py
├── logs/
└── Organized/ (created after execution)
```


---

## ⚙️ How It Works

1. Scans all files in the given directory  
2. Generates hash for each file  
3. Detects duplicates based on hash  
4. Moves files into categorized folders  
5. Renames files if name conflict occurs  

---

## ▶️ Usage

### 🔹 Dry Run (Safe Mode)

```bash
python main.py --path "your-folder-path" --dry-run
```

👉 Shows what will happen without making changes  

---

### 🔹 Real Execution

```bash
python main.py --path "your-folder-path"
```

👉 Organizes files and moves them into folders  

## 📂 Output Example

```
TestFolder/
│
├── Organized/
│   ├── Images/
│   ├── Videos/
│   ├── Documents/
│   ├── Audio/
│   └── Duplicates/
```

---

## 📝 Logging

All operations are recorded in:

```
logs/log.txt
```
⚠️ Notes
Avoid running on important folders without dry-run
Duplicate detection is based on file content (not name)
Empty files may produce identical hashes

---

## 👤 Author

**Dhyan Patel**  
📌 GitHub: https://github.com/DhyanPr


---

import os
import shutil
from config import FILE_TYPES
from duplicate_finder import get_file_hash
from logger import log


class FileOrganizer:
    def __init__(self, path, dry_run=False):
        self.path = path
        self.dry_run = dry_run
        self.hash_map = {}
        self.output_path = os.path.join(self.path, "Organized")

        # ✅ For UI tracking
        self.progress = 0
        self.logs = []
        self.error = None

    def organize(self):
        if not os.path.exists(self.path):
            self.error = "Invalid path!"
            return

        total_files = self.count_files()
        if total_files == 0:
            self.error = "Folder is empty!"
            return

        processed = 0
        print(f"Organizing files in: {self.path}\n")

        for root, _, files in os.walk(self.path):

            # 🚫 Skip Organized folder
            if root.startswith(self.output_path):
                continue

            for file in files:
                full_path = os.path.join(root, file)

                if os.path.isfile(full_path):
                    try:
                        file_hash = get_file_hash(full_path)

                        if file_hash is not None:
                            if file_hash in self.hash_map:
                                self.handle_duplicate(full_path)
                            else:
                                self.hash_map[file_hash] = full_path
                                folder = self.get_folder(file)
                                self.move_file(full_path, folder)
                        else:
                            folder = self.get_folder(file)
                            self.move_file(full_path, folder)

                        processed += 1
                        self.show_progress(processed, total_files)

                    except Exception as e:
                        self.error = str(e)
                        log(f"Error processing {file}: {e}")

        # ✅ VERY IMPORTANT
        self.progress = 100
        print("\n✅ Organization Complete!")

    def get_folder(self, filename):
        ext = os.path.splitext(filename)[1].lower()

        for folder, extensions in FILE_TYPES.items():
            if ext in extensions:
                return folder

        return "Others"

    def move_file(self, src, folder):
        dest_folder = os.path.join(self.output_path, folder)
        file_name = os.path.basename(src)
        dest_path = os.path.join(dest_folder, file_name)

        dest_path = self.handle_rename(dest_path)

        if self.dry_run:
            message = f"[DRY-RUN] Would move: {src} -> {dest_path}"
            print(message)
        else:
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(src, dest_path)
            message = f"[MOVED] {src} -> {dest_path}"

        log(message)
        self.logs.append(message)

    def handle_duplicate(self, file_path):
        dup_folder = os.path.join(self.output_path, "Duplicates")
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(dup_folder, file_name)

        dest_path = self.handle_rename(dest_path)

        if self.dry_run:
            message = f"[DRY-RUN] Would move duplicate: {file_path} -> {dest_path}"
            print(message)
        else:
            os.makedirs(dup_folder, exist_ok=True)
            shutil.move(file_path, dest_path)
            message = f"[DUPLICATE] {file_path} -> {dest_path}"

        log(message)
        self.logs.append(message)

    def handle_rename(self, path):
        base, ext = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = f"{base}_{counter}{ext}"
            counter += 1

        return path

    def count_files(self):
        count = 0
        for root, _, files in os.walk(self.path):
            if root.startswith(self.output_path):
                continue
            count += len(files)
        return count

    def show_progress(self, processed, total):
        if total == 0:
            return

        percent = int((processed / total) * 100)
        self.progress = percent

        print(f"\rProcessing: {percent}% ({processed}/{total})", end="")
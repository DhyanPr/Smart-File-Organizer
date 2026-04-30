import argparse
from organizer import FileOrganizer

def main():
    parser = argparse.ArgumentParser(description="Smart File Organizer")
    parser.add_argument("--path", required=True, help="Folder path to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")

    args = parser.parse_args()

    organizer = FileOrganizer(args.path, dry_run=args.dry_run)
    organizer.organize()

    print("✅ Organization complete! Check logs for details.")

if __name__ == "__main__":
    main()
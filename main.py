import os
import argparse
from tabulate import tabulate

def format_size(size_bytes, unit):
    if unit == 'bytes':
        return f"{size_bytes} B"
    elif unit == 'kb':
        return f"{size_bytes / 1024:.2f} KB"
    elif unit == 'mb':
        return f"{size_bytes / (1024**2):.2f} MB"
    elif unit == 'gb':
        return f"{size_bytes / (1024**3):.2f} GB"
    else:  # auto
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / (1024**2):.2f} MB"
        else:
            return f"{size_bytes / (1024**3):.2f} GB"

def is_hidden(name):
    return name.startswith('.') or name.startswith('~')

def scan_folder(path, args, depth=0):
    folder_size = 0
    items_to_display = []

    try:
        with os.scandir(path) as entries:
            for entry in entries:
                try:
                    if not args.hidden and is_hidden(entry.name):
                        continue

                    entry_path = os.path.join(path, entry.name)

                    if entry.is_file(follow_symlinks=False):
                        ext = os.path.splitext(entry.name)[1].lower()
                        if args.exclude_ext and ext in args.exclude_ext:
                            continue

                        size = entry.stat(follow_symlinks=False).st_size
                        if size >= args.min_size:
                            folder_size += size
                            # Only display file if details are required and within max-depth
                            if args.details and (args.max_depth is None or depth <= args.max_depth):
                                items_to_display.append([path, entry.name, size])

                    elif entry.is_dir(follow_symlinks=False):
                        sub_items, sub_size = scan_folder(entry_path, args, depth + 1)
                        folder_size += sub_size
                        # Only add display if within max-depth
                        if args.max_depth is None or depth + 1 <= args.max_depth:
                            items_to_display.extend(sub_items)

                except Exception as e:
                    if args.details and (args.max_depth is None or depth <= args.max_depth):
                        items_to_display.append([path, entry.name, f"Error: {e}"])
    except Exception as e:
        print(f"⚠️ Cannot access: {path} - {e}")

    # Add current folder if within display limit
    if not args.details and (args.max_depth is None or depth <= args.max_depth):
        items_to_display.append([path, '', folder_size])

    return items_to_display, folder_size

def main():
    parser = argparse.ArgumentParser(description="View the size of folders, subfolders, and files.")
    parser.add_argument("path", help="Target folder path")
    parser.add_argument("-u", "--unit", choices=["auto", "bytes", "kb", "mb", "gb"], default="auto", help="Size unit")
    parser.add_argument("-d", "--details", action="store_true", help="Show all files (not just folders)")
    parser.add_argument("-t", "--total-only", action="store_true", help="Show only the total size")
    parser.add_argument("--max-depth", type=int, help="Limit the folder depth")
    parser.add_argument("--min-size", type=int, default=1, help="Minimum file size (in bytes) to count")
    parser.add_argument("--exclude-ext", nargs="*", help="Exclude files with these extensions (e.g., .tmp .log)")
    parser.add_argument("--hidden", action="store_true", help="Include hidden files/folders")

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"❌ Invalid path: {args.path}")
        return

    results, total_size = scan_folder(args.path, args)

    if args.total_only:
        print(f"\n📦 Total size of all: {format_size(total_size, args.unit)}")
    else:
        formatted = []
        for row in results:
            name = row[1] if row[1] else "<DIR>"
            size = row[2]
            if isinstance(size, int):
                size = format_size(size, args.unit)
            formatted.append([row[0], name, size])

        print(tabulate(formatted, headers=["Path", "Name", "Size"], tablefmt="github"))
        print(f"\n📦 Total size of all: {format_size(total_size, args.unit)}")

if __name__ == "__main__":
    main()

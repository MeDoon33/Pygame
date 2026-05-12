import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Dice import read_text_content, is_file_empty, is_text_file
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Test reading the file
file_path = "questions_sample.txt"
print(f"Testing file: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")
print(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'}")

if os.path.exists(file_path):
    # Test is_file_empty
    empty = is_file_empty(file_path)
    print(f"Is file empty: {empty}")

    # Test is_text_file
    is_text = is_text_file(file_path)
    print(f"Is text file: {is_text}")

    # Test read_text_content
    success, content = read_text_content(file_path)
    print(f"Read success: {success}")

    if success:
        # Write content to file with UTF-8 encoding
        with open("debug_content.txt", "w", encoding="utf-8") as f:
            f.write("=== CONTENT START ===\n")
            f.write(content)
            f.write("\n=== CONTENT END ===")
        print("Content written to debug_content.txt")

        # Print first 200 characters
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"Content preview: {preview}")
    else:
        print(f"Read error: {content}")
else:
    print("File does not exist")
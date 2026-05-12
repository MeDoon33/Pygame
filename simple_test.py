import os
import sys

# Test basic file operations without printing to terminal
try:
    # Test file existence
    file_path = "questions_sample.txt"
    exists = os.path.exists(file_path)
    size = os.path.getsize(file_path) if exists else 0

    # Test reading with different encodings
    results = []

    if exists:
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                    content = f.read()
                # Check for replacement characters
                has_replacement = '\ufffd' in content
                results.append(f"{encoding}: success, replacement_chars={has_replacement}, length={len(content)}")
            except Exception as e:
                results.append(f"{encoding}: failed - {str(e)}")

    # Write results to file
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write(f"File exists: {exists}\n")
        f.write(f"File size: {size}\n")
        f.write("Encoding tests:\n")
        for result in results:
            f.write(f"  {result}\n")

    # Success marker
    with open("test_success.txt", "w", encoding="utf-8") as f:
        f.write("Test completed successfully")

except Exception as e:
    # Write error to file
    with open("test_error.txt", "w", encoding="utf-8") as f:
        f.write(f"Error: {str(e)}")
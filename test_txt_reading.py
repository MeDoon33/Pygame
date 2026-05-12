#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra đọc file .txt
"""

import os
import sys

def test_read_questions_sample():
    """Test đọc file questions_sample.txt"""
    print("=" * 60)
    print("TEST: Reading questions_sample.txt")
    print("=" * 60)

    file_path = "questions_sample.txt"

    if not os.path.exists(file_path):
        print(f"[FAIL] File {file_path} does not exist")
        return False

    print(f"[OK] File exists: {file_path}")

    # Test multiple encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                content = f.read()
            print(f"[OK] Successfully read with {encoding.upper()}")
            print(f"Content length: {len(content)} characters")
            print("First 200 characters:")
            print(repr(content[:200]))
            print()

            # Check for Vietnamese characters
            if 'Python' in content and ('được' in content or 'phát triển' in content):
                print(f"[OK] Vietnamese characters detected with {encoding.upper()}")
                return True
            else:
                print(f"[WARN] No Vietnamese characters found with {encoding.upper()}")

        except UnicodeDecodeError as e:
            print(f"[FAIL] {encoding.upper()} failed: {e}")
        except Exception as e:
            print(f"[ERROR] {encoding.upper()} error: {e}")

    # Try with errors='ignore'
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if content.strip():
            print("[OK] Read with errors='ignore'")
            print(f"Content length: {len(content)} characters")
            return True
    except Exception as e:
        print(f"[FAIL] Even errors='ignore' failed: {e}")

    return False

def test_import_function():
    """Test hàm import_questions_from_file"""
    print("\n" + "=" * 60)
    print("TEST: import_questions_from_file function")
    print("=" * 60)

    try:
        # Import the function
        from Dice import import_questions_from_file

        result = import_questions_from_file("questions_sample.txt")

        if result:
            print(f"[OK] Import successful: {len(result)} questions")
            for i, q in enumerate(result[:2]):  # Show first 2 questions
                print(f"  Question {i+1}: {q['text'][:50]}...")
        else:
            print("[FAIL] Import returned empty list")

        return len(result) > 0

    except Exception as e:
        print(f"[FAIL] Import function error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing .txt file reading...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()

    success1 = test_read_questions_sample()
    success2 = test_import_function()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILURE] Some tests failed!")
    print("=" * 60)
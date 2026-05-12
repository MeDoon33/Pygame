#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script để kiểm tra encoding của file questions_sample.txt
"""

import os
import sys

def detect_encoding(file_path):
    """Detect encoding of a file"""
    try:
        # Try to import chardet
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result
    except ImportError:
        print("chardet not installed, trying manual detection...")
        return manual_encoding_detect(file_path)

def manual_encoding_detect(file_path):
    """Manual encoding detection"""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                content = f.read(1000)  # Read first 1000 chars
            return {'encoding': encoding, 'confidence': 1.0}
        except UnicodeDecodeError:
            continue

    return {'encoding': 'unknown', 'confidence': 0.0}

def test_file_reading():
    """Test reading the file with different encodings"""
    file_path = "questions_sample.txt"

    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} does not exist!")
        return False

    print(f"File exists: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")

    # Detect encoding
    encoding_info = detect_encoding(file_path)
    print(f"Detected encoding: {encoding_info}")

    # Try reading with detected encoding
    detected_encoding = encoding_info.get('encoding', 'utf-8')

    try:
        with open(file_path, 'r', encoding=detected_encoding, errors='strict') as f:
            content = f.read()
        print("SUCCESS: Read with detected encoding")
        print(f"Content length: {len(content)}")
        print("First 200 characters:")
        print(repr(content[:200]))
        return True
    except Exception as e:
        print(f"FAILED: Could not read with {detected_encoding}: {e}")

        # Try fallback encodings
        fallback_encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for enc in fallback_encodings:
            if enc == detected_encoding:
                continue
            try:
                with open(file_path, 'r', encoding=enc, errors='strict') as f:
                    content = f.read()
                print(f"SUCCESS: Read with fallback {enc}")
                print(f"Content length: {len(content)}")
                return True
            except:
                continue

        # Last resort: errors='ignore'
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if content.strip():
                print("SUCCESS: Read with errors='ignore'")
                print(f"Content length: {len(content)}")
                return True
        except Exception as e:
            print(f"FAILED: Even errors='ignore' failed: {e}")

    return False

def test_import_function():
    """Test the actual import function"""
    print("\n" + "="*50)
    print("Testing import_questions_from_file")
    print("="*50)

    try:
        # Import the function
        sys.path.insert(0, os.getcwd())
        from Dice import import_questions_from_file

        questions = import_questions_from_file("questions_sample.txt")

        if questions and len(questions) > 0:
            print(f"SUCCESS: Imported {len(questions)} questions")
            return True
        else:
            print("FAILED: No questions imported")
            return False

    except Exception as e:
        print(f"ERROR in import function: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Debugging .txt file reading issues")
    print(f"Python: {sys.version}")
    print(f"Current dir: {os.getcwd()}")
    print()

    success1 = test_file_reading()
    success2 = test_import_function()

    print("\n" + "="*50)
    if success1 and success2:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("="*50)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script that writes results to file instead of terminal
"""

import os
import sys

def test_file_reading():
    """Test reading questions_sample.txt and write results to file"""
    results = []
    results.append("=" * 60)
    results.append("TEST: Reading questions_sample.txt")
    results.append("=" * 60)

    file_path = "questions_sample.txt"

    if not os.path.exists(file_path):
        results.append(f"[FAIL] File {file_path} does not exist")
        return results

    results.append(f"[OK] File exists: {file_path}")
    results.append(f"File size: {os.path.getsize(file_path)} bytes")

    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                content = f.read()
            results.append(f"[OK] Successfully read with {encoding.upper()}")
            results.append(f"Content length: {len(content)} characters")

            # Check for Vietnamese content
            if 'Python' in content and ('được' in content or 'phát triển' in content):
                results.append(f"[OK] Vietnamese characters found with {encoding.upper()}")
                results.append("First 200 characters:")
                results.append(repr(content[:200]))
                break
            else:
                results.append(f"[WARN] No Vietnamese characters with {encoding.upper()}")

        except UnicodeDecodeError as e:
            results.append(f"[FAIL] {encoding.upper()} failed: {e}")
        except Exception as e:
            results.append(f"[ERROR] {encoding.upper()} error: {e}")

    return results

def test_import_function():
    """Test the import function"""
    results = []
    results.append("\n" + "=" * 60)
    results.append("TEST: import_questions_from_file function")
    results.append("=" * 60)

    try:
        # Import the function
        sys.path.insert(0, os.getcwd())
        from Dice import import_questions_from_file

        questions = import_questions_from_file("questions_sample.txt")

        if questions and len(questions) > 0:
            results.append(f"[OK] Import successful: {len(questions)} questions")
            for i, q in enumerate(questions[:2]):
                results.append(f"  Question {i+1}: {q['text'][:50]}...")
        else:
            results.append("[FAIL] Import returned empty list")

    except Exception as e:
        results.append(f"[FAIL] Import function error: {e}")
        import traceback
        results.append(traceback.format_exc())

    return results

if __name__ == "__main__":
    all_results = []
    all_results.append("Debugging .txt file reading issues")
    all_results.append(f"Python: {sys.version}")
    all_results.append(f"Current dir: {os.getcwd()}")
    all_results.append("")

    all_results.extend(test_file_reading())
    all_results.extend(test_import_function())

    all_results.append("\n" + "=" * 60)
    all_results.append("DEBUG RESULTS WRITTEN TO FILE")
    all_results.append("=" * 60)

    # Write results to file
    with open("debug_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_results))

    print("Results written to debug_results.txt")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal test for import function
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from Dice import import_questions_from_file
    print("Import successful")

    questions = import_questions_from_file("questions_sample.txt")
    print(f"Questions imported: {len(questions) if questions else 0}")

    if questions:
        print("First question:", questions[0]['text'][:50])
        print("SUCCESS")
    else:
        print("FAILED: No questions")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
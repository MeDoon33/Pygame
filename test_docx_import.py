import sys
sys.path.append('.')
from Dice import import_questions_from_file
result = import_questions_from_file('test_questions.docx')
print(f'Number of questions imported: {len(result)}')
for i, q in enumerate(result):
    print(f'Question {i+1}: {q["text"]}')
    print(f'Options: {q["options"]}')
    print(f'Correct: {q["correct"]}')
# 🚀 QUICK START: Enhanced Question Import

## What's New?

Previously: Only .txt files supported
Now: ✅ .txt, ✅ .doc, ✅ .docx supported

Plus automatic validation:
- ✅ Detects empty files
- ✅ Validates file is text (not image/video/zip)
- ✅ Checks question format
- ✅ Clear error messages

---

## 📝 One-Minute Setup

### For .txt files (always works)
```
1. Create questions in any text editor
2. Game Menu → "Tao cau hoi tu file"
3. Select your .txt file
4. Done! Questions are imported
```

### For .docx files (optional setup)

**First time only:**
```bash
pip install python-docx
```

**Then use:**
```
1. Create questions in Microsoft Word
2. Save as .docx
3. Game Menu → "Tao cau hoi tu file"  
4. Select your .docx file
5. Done! Questions are imported
```

---

## ✅ Error Messages You Might See

| Message | Meaning | Fix |
|---------|---------|-----|
| "[FAIL] File rong" | File is empty | Add content to file |
| "[FAIL] File khong phai van ban" | File is binary/image/video | Use .txt, .doc, or .docx |
| "[FAIL] Khong tim thay cau hoi hop le" | Format is wrong | Follow template below |
| "[WARN] python-docx chua cai dat" | Can't read .docx files | Run: `pip install python-docx` |

---

## 📄 Question Format Template

```
Python la gi?
Framework web
Ngon ngu lap trinh  
Database
Operating system
Correct: 2
Reward: Sat thuong +50%

[BLANK LINE - Important!]

Tiep theo...
Option 1
Option 2  
Option 3
Option 4
Correct: 1
Reward: Hoi mau 50HP
```

**Rules:**
- Line 1: Question (must end with ?)
- Lines 2-5: 4 answer options  
- Line 6: Correct: [1-4]
- Line 7: Reward: [description]
- Line 8: Blank line separates questions

---

## 🎯 Test It Now

**Step 1:** Open game
```bash
python Dice.py
```

**Step 2:** Click "Tao cau hoi tu file"

**Step 3:** Choose `questions_sample.txt`

**Expected Result:**
```
[OK] Thanh cong: Tim thay 5 cau hoi
```

---

## 📚 Files to Read

- **IMPORT_QUESTIONS_GUIDE.md** - Full guide with examples
- **ENHANCEMENT_SUMMARY.md** - Technical details
- **questions_sample.txt** - Example questions
- **QUESTIONS_IMPORT_TESTING.md** - Test cases

---

## 🛠️ Need .docx/.doc Support?

```bash
# Install the library (one time)
pip install python-docx

# Verify it works
python -c "from docx import Document; print('OK')"
```

**Without it:** Only .txt files work (still perfectly fine!)

---

## 🔧 Troubleshooting in 30 Seconds

**Problem:** Import fails
1. Check file is not empty
2. Check file is .txt, .doc, or .docx  
3. Check question format (see template above)
4. Read the error message - it tells you exactly what's wrong

**Problem:** .docx files won't load
1. Install: `pip install python-docx`
2. Try again

**Problem:** Vietnamese characters look wrong  
1. Make sure file is saved as UTF-8
2. In VS Code: Bottom right → UTF-8
3. In Notepad: File → Save As → UTF-8

---

## ✨ What Works Now

✅ Import .txt questions
✅ Import .doc questions (with python-docx)
✅ Import .docx questions (with python-docx)
✅ Empty file detection
✅ Binary file rejection
✅ Bad format detection
✅ UTF-8 encoding support
✅ Clear error messages
✅ Graceful handling of mixed valid/invalid questions

---

## 🎮 Try Different File Formats

**Option 1: Text Editor (.txt)**
- Quick & simple
- Works everywhere  
- Use: Notepad, VS Code, Sublime

**Option 2: Microsoft Word (.docx)**
- Visual editing
- Need: `pip install python-docx`
- File → Save As → .docx format

**Option 3: Old Word (.doc)**
- Very old Word files
- Need: `pip install python-docx`
- Less common now

---

## 📞 Still Have Questions?

1. **Check file format**: Compare with `questions_sample.txt`
2. **Read error message**: It tells you exactly what's wrong
3. **Install python-docx**: `pip install python-docx`
4. **Try .txt first**: Always works, no setup needed

---

## 🎉 You're All Set!

Your Dice Roguelite now supports:
- Multiple file formats (.txt, .doc, .docx)
- Automatic file validation  
- Clear error messages
- Seamless import experience

**Enjoy importing your custom questions!**


# Fix Import Error - Quick Solution

If you're seeing this error when running `streamlit run web_ui/app.py`:

```
ModuleNotFoundError: No module named 'google.genai'
```

## Solution

Run these commands in your terminal:

```bash
# 1. Uninstall any old Google packages
pip uninstall google-generativeai google-genai -y

# 2. Install the correct package
pip install google-genai>=0.2.0

# 3. Install all other requirements
pip install -r requirements.txt

# 4. Verify installation
python -c "from google import genai; print('✓ google-genai installed correctly')"
```

## If That Doesn't Work

Try creating a fresh virtual environment:

```bash
# Create new virtual environment
python -m venv venv_new

# Activate it
source venv_new/bin/activate  # On Mac/Linux
# or
venv_new\Scripts\activate  # On Windows

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Test import
python -c "from google import genai; print('✓ Works!')"

# Now run the app
streamlit run web_ui/app.py
```

## About the SDK

- **Package:** `google-genai` (NEW, recommended)
- **Old Package:** `google-generativeai` (being deprecated)
- **Import:** `from google import genai`

The Google GenAI SDK became GA in May 2025 and is the official way to use Gemini API with file search.

## Verify Your Installation

After installing, check that you can import correctly:

```python
python
>>> from google import genai
>>> from google.genai import types
>>> print("Success!")
```

If you see "Success!" - you're ready to run the app!

## Still Having Issues?

1. Check your Python version:
   ```bash
   python --version  # Should be 3.9+
   ```

2. Make sure you're in the project directory:
   ```bash
   cd /path/to/LENR-Google
   ```

3. Check that requirements.txt has:
   ```
   google-genai>=0.2.0
   ```

4. Try upgrading pip:
   ```bash
   pip install --upgrade pip
   ```

## After Fixing

Once installed, start the app:

```bash
streamlit run web_ui/app.py
```

Your browser should open to `http://localhost:8501` and the app should load without errors!

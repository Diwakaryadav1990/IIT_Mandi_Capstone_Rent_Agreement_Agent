# Setup and Run Instructions

This document explains how to set up your environment and run the Apartment Rental Agreement Red Flag Agent.

## 1. Setting up the Python Environment (Recommended)

It is highly recommended to use a virtual environment to manage dependencies.

**Open your terminal (PowerShell or Command Prompt) and navigate to the project directory:**
```bash
cd D:\Assignements\Capstone_Rental_Agreement_redflag
```

**Create a virtual environment named `venv`:**
```bash
python -m venv venv
```

**Activate the virtual environment:**
- On **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- On **Windows (Command Prompt)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```

*(You will know it's activated when you see `(venv)` at the beginning of your command line prompt.)*

## 2. Installing Dependencies

Once the environment is active, install the required packages:

```bash
pip install -r requirements.txt
```

## 3. Running the Application

Sometimes, depending on your Python installation on Windows, installed scripts (like `streamlit`) might not automatically be added to your system's PATH. 

**If you see an error like:**
> `streamlit : The term 'streamlit' is not recognized as the name of a cmdlet...`

**Use the following command to run the app instead:**
```bash
python -m streamlit run main.py
```

*This tells Python to directly find and run the streamlit module, bypassing the PATH issue.*

If `streamlit run app.py` works for you without issues, you can continue using that.

## 4. Providing the Gemini API Key

You need a Gemini API key to perform analyses. You have two options:

**Option A: Through the UI (Easiest)**
1. Run the app using the command above.
2. Look at the left sidebar in the web interface.
3. Paste your Gemini API key into the input field.

**Option B: Environment Variable (Advanced)**
1. Create a file named `.env` in the root of your project folder (`D:\Assignements\Capstone_Rental_Agreement_redflag`).
2. Add the following line to the file, replacing `your_api_key_here` with your actual key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. Save the file. The app will automatically read this key when it starts.

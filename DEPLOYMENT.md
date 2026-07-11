# Deployment & Hosting Guide

This guide will walk you through uploading your code to GitHub and hosting it for free on Streamlit Community Cloud.

## Step 1: Uploading to GitHub

Since you do not have `git` installed on your machine, the easiest way to upload your code is using the GitHub website directly.

1. **Log in to GitHub:** Go to [github.com](https://github.com/) and log in to your account.
2. **Create a New Repository:** 
   - Click the **"+"** icon in the top right corner and select **"New repository"**.
   - Name your repository (e.g., `rental-agreement-agent`).
   - Choose whether you want it to be **Public** or **Private** (Public is usually easier for free hosting, but Streamlit Community Cloud supports Private repos as well if you connect your account).
   - *Do not* check the boxes to initialize with a README, .gitignore, or license (we already have those files ready).
   - Click **"Create repository"**.
3. **Upload Files:**
   - On the next screen, look for the link that says **"uploading an existing file"** (it is usually a small link below the quick setup instructions). Click it.
   - Open your project folder on your computer: `D:\Assignements\Capstone_Rental_Agreement_redflag`
   - **Drag and drop** all the files and folders from your project directory into the GitHub website upload area.
     *Make sure you include:*
     - `core/` folder
     - `ui/` folder
     - `utils/` folder
     - `sample_agreements/` folder
     - `main.py`
     - `requirements.txt`
     - `SETUP.md`
     - `.gitignore` (if you can see hidden files)
     *(Do **not** upload the `venv` folder or the `logs.db` file, though the `.gitignore` should try to block them anyway if you were using git).*
   - Once the files finish uploading, scroll down and click the green **"Commit changes"** button.

## Step 2: Hosting on Streamlit Community Cloud

Now that your code is on GitHub, deploying it is very straightforward.

1. **Go to Streamlit Community Cloud:** Visit [share.streamlit.io](https://share.streamlit.io/) and log in. (You can sign in with your GitHub account).
2. **Deploy an App:**
   - Click the **"New app"** button.
   - If prompted, authorize Streamlit to access your GitHub repositories.
   - You will see a form to fill out:
     - **Repository:** Select the repository you just created (e.g., `yourusername/rental-agreement-agent`).
     - **Branch:** Select `main` (or `master`).
     - **Main file path:** Type `main.py` (this is crucial since we changed it from `app.py`).
     - **App URL:** You can customize the URL or leave it as the default.
3. **Deploy!** Click the **"Deploy!"** button.
   - Streamlit will now read your `requirements.txt`, install the packages, and launch your app. This might take a minute or two.
4. **The API Key:** Since we implemented the popup dialog (`@st.dialog`) in `main.py`, anyone who visits your public URL will be prompted to enter their own Gemini API key before they can use the agent. This ensures your personal key is kept safe and you are not paying for others' usage.

Congratulations! Your app should now be live on the internet!

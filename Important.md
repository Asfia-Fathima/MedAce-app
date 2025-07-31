⚠️ IMPORTANT NOTICE FOR FUTURE CONTRIBUTORS & USERS
Welcome to MedAce – a smart,AI-assisted medical companion built using Streamlit and integrated with LLMs via API.

#  Security First: Handle Secrets Responsibly
This project uses API keys stored in .streamlit/secrets.toml. Do NOT commit this file to GitHub or any public VCS.

Always add .streamlit/secrets.toml to .gitignore

Never hardcoode secrets inside Python files

For deployment, use environment variables or secrets.toml in Streamlit Cloud only

If a secret acidentally gets committed:

Revoke it immediately

Follow GitHub’s push protection guidelines

#  Setup Advice
Clone this repo into a fresh, isolated Python environment (e.g., using venv)

Run: pip install -r requirements.txt

Ensure your secrets.toml is configured locally for testing

Launch with: streamlit run app.py

Version Control Guidelines
Use feature branches

Pull before you push (git pull origin main --rebase)

Write meaningful commit messages

Never force-push to main unless you're absolutely sure

# For Deployers & Forkers
If you’re planning to deploy or fork this project:

Replace API keys with your own

Sanitize all config files before making your repo public

Review dependencies in requirements.txt to avoid security vulnerabilities

“With great AI comes great responsibility.”
—Amisstrie

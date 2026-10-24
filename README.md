🔐 Vaultora — Intelligent Document Security & Sharing

Secure. Share. Verify. Trust.

TrustVault is a Flask-based document-sharing application designed to help organizations share files securely. It includes company-level access control, role-based permissions, SHA-256 file integrity verification, and audit logging.

<p align="center">🚀 Live Demo: https://trustvault-xuxn.onrender.com/

💻 GitHub Repository: https://github.com/Hemalatha24574/TrustVault

</p>---

✨ Key Features

- 🔑 User Authentication — Register and log in to access the application.
- 🏢 Company-Level Isolation — Restricts document access based on company membership.
- 👥 Controlled File Sharing — Share documents with registered users in the same company.
- 🛡️ Role-Based Access Control — Provides different permissions for administrators and regular users.
- 🔍 SHA-256 Integrity Verification — Checks file integrity before allowing downloads.
- 📋 Audit Logging — Records important activities such as uploads, sharing, and downloads.
- 📂 Document Management — Upload, access, and download authorized documents.

🛠️ Tech Stack

Technology| Purpose
Python| Application logic
Flask| Web framework
SQLite| Database
HTML & CSS| User interface
SHA-256| File integrity verification
Git & GitHub| Version control
Render| Web application hosting

⚙️ Run Locally

Prerequisites

- Python 3
- Git (optional if downloading the ZIP)
- A terminal

Installation

1. Clone the repository

git clone https://github.com/Hemalatha24574/TrustVault.git
cd TrustVault

2. Create and activate a virtual environment

Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

Windows:

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

python3 -m pip install -r requirements.txt

4. Configure environment variables

Set a strong, unique "SECRET_KEY" and configure the admin credentials using the instructions in the project documentation. Never commit passwords, secret keys, or ".env" files to GitHub.

5. Start the application

python3 app.py

6. Open the application

Visit http://127.0.0.1:5000/ in your browser.

🔐 Security Considerations

- Users must authenticate before accessing protected functionality.
- Document access is restricted by ownership, sharing permissions, company membership, and role.
- SHA-256 hashes are used to detect changes to stored files.
- Administrative audit information is restricted to authorized administrators.
- The current free hosting setup may use ephemeral storage. Uploaded files and database records may not survive restarts or redeployments.

Note: This is an educational project and has not undergone a professional security audit. Do not upload confidential documents or use it for sensitive production workloads without further security hardening and reliable persistent storage.

🚧 Future Improvements

- Add automated tests for access-control and security edge cases.
- Configure persistent database and file storage.
- Add CSRF protection and rate limiting.
- Improve document search and audit-log filtering.
- Enhance the user interface and error handling.

👩‍💻 Project Information

Project: TrustVault — Secure Document Sharing
Category: Web Application / Information Security
Deployment: Render

---

Built as a project to explore secure file sharing, access control, and document integrity verification.

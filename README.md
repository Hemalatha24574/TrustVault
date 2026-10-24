🔐 TrustVault — Secure Document Sharing

📌 Overview

Vaultora is a Flask-based document-sharing application designed to help organizations manage and share documents with controlled access.

It combines user authentication, company-level access restrictions, role-based permissions, SHA-256 file integrity verification, and audit logging to make document sharing more secure and transparent.

The project demonstrates concepts used in:

- Enterprise document management
- Secure file-sharing systems
- Role-based access control
- File integrity verification
- Activity monitoring and auditing

---

🚀 Live Demo & Source Code

- 🌐 Live Demo: https://trustvault-xuxn.onrender.com/
- 💻 GitHub Repository: https://github.com/Hemalatha24574/TrustVault

---

🎯 Features

✔ User registration and login
✔ Company-level document access restrictions
✔ Document upload and download
✔ Controlled sharing with registered users in the same company
✔ Role-based permissions for administrators and regular users
✔ SHA-256 hash verification before document downloads
✔ Audit logging for important document activities
✔ Access restrictions for unauthorized users
✔ Flask-based web interface
✔ SQLite database integration

---

🔄 System Workflow

1. User Authentication

- Users register and log in to the application.
- Protected features require authentication.

2. Document Upload

- An authorized user uploads a document.
- The application stores document information and calculates its SHA-256 hash.

3. Access Control

- Document access is checked using ownership, sharing permissions, company membership, and user role.
- Users cannot access documents merely because they know a document's URL.

4. Document Sharing

- The document owner can share a document with a registered user in the same company.
- The recipient can access the document if the sharing permission allows it.

5. Integrity Verification

- The application calculates the file's SHA-256 hash before downloading.
- The calculated hash is compared with the stored hash.
- A mismatch is treated as an integrity failure.

6. Audit Logging

- Important actions, such as uploads, sharing, downloads, and access denials, can be recorded in the audit trail.
- Authorized administrators can review audit information.

---

🛡️ Security Features

Feature| Purpose
Authentication| Protects restricted application functionality
Company-level isolation| Restricts access across different companies
Ownership checks| Controls who can share a document
Sharing permissions| Allows authorized recipients to access shared files
Role-based access| Separates administrator and regular-user permissions
SHA-256 verification| Detects unexpected changes to stored files
Audit logging| Helps track important application activities

Important: Vaultora is an educational project and has not undergone a professional security audit. It should not be used for confidential documents or sensitive production workloads without further security hardening.

---

🛠️ Technologies Used

- Python 3 — Backend programming
- Flask — Web application framework
- SQLite — Database
- HTML & CSS — User interface
- SHA-256 — File integrity verification
- Git & GitHub — Version control and source-code hosting
- Render — Web application deployment

---

📂 Project Structure

TrustVault/
│
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── PROMPTS.md
│
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── audit.html
    └── error.html

---

▶️ How to Run Locally

Prerequisites

- Python 3
- Git, or download the repository as a ZIP
- A terminal

Step 1: Clone the repository

git clone https://github.com/Hemalatha24574/TrustVault.git
cd TrustVault

Step 2: Create a virtual environment

Linux / macOS / Chromebook Linux:

python3 -m venv .venv
source .venv/bin/activate

Windows:

python -m venv .venv
.venv\Scripts\activate

Step 3: Install dependencies

python3 -m pip install -r requirements.txt

Step 4: Configure environment variables

Configure a strong, unique "SECRET_KEY" and the required administrator credentials using the project's setup instructions.

Never publish passwords, secret keys, or ".env" files.

Step 5: Start the application

python3 app.py

Step 6: Open the application

Visit:

"http://127.0.0.1:5000/" (http://127.0.0.1:5000/)

---

📋 Example Workflow

1. Register a user account and log in.
2. Upload a sample document.
3. Share the document with a registered user in the same company.
4. Log in as the recipient and verify access to the shared document.
5. Download the document and check the integrity-verification result.
6. Review the recorded activities through the authorized admin audit interface.

---

💾 Database & Storage

Vaultora uses SQLite to store application records and local file storage for uploaded documents.

Deployment limitation: The current hosting setup may use ephemeral storage. Database records and uploaded files may disappear after restarts or redeployments. Persistent database and file storage should be configured and tested before relying on long-term storage.

---

🚧 Future Enhancements

- Automated tests for access-control edge cases
- Persistent database and object storage
- CSRF protection and rate limiting
- Improved document search and audit-log filtering
- Enhanced error handling and user-interface feedback
- Additional deployment and security hardening

---

👩‍💻 Author

Developed as a Python and Flask project to explore secure document sharing, access control, file integrity verification, and audit logging.

---

⭐ Vaultora — Secure Document Sharing with Integrity Verification and Access Control.
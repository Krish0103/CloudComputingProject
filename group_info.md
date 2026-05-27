# 📋 Group 6 — Submission File

## 🗂️ Project Details

| Field              | Details                          |
|--------------------|----------------------------------|
| **Group Number**   | Group 6                         |
| **Project Name**   | SecureWeb Vulnerability Lab      |
| **Reference Used** | learning/cyber_security/password-strength-checker|
| **Branch Name**    | grp6-secureweb-vulnerability-lab |
| **Deployed URL**   | <!-- Paste your live deployment link here --> |

---

## �� Student Details

### 🧑‍💻 Student 1

| Field             | Details                        |
|-------------------|--------------------------------|
| **Full Name**     | Krish Aggarwal                 |
| **Roll Number**   | 2310991876                     |
| **GitHub Profile**| https://github.com/Krish0103   |
| **Contribution**  | Developed the Secure Authentication Flow using bcrypt and JWT session management. |

---

### 🧑‍💻 Student 2

| Field             | Details                        |
|-------------------|--------------------------------|
| **Full Name**     | Jiya Kukreja                   |
| **Roll Number**   | 2310991860                     |
| **GitHub Profile**| https://github.com/Jiyakukreja |
| **Contribution**  | Implemented the Custom Password Strength Enforcement and dictionary password rejection. |

---

### 🧑‍💻 Student 3

| Field             | Details                        |
|-------------------|--------------------------------|
| **Full Name**     | Jatin Seth                     |
| **Roll Number**   | 2310991859                     |
| **GitHub Profile**| https://github.com/Jatin-Seth  |
| **Contribution**  | Built the Brute-Force Defense and Logging mechanism to detect and alert on rapid failed logins. |

---

### 🧑‍💻 Student 4

| Field             | Details                         |
|-------------------|---------------------------------|
| **Full Name**     | Kartikeya Jain                  |
| **Roll Number**   | 2310991865                      |
| **GitHub Profile**| https://github.com/kartikeya1911|
| **Contribution**  | Designed the Zero-Configuration SQLite database and implemented parameterized queries to prevent SQL Injection. |

---

### 🧑‍💻 Student 5

| Field             | Details                        |
|-------------------|--------------------------------|
| **Full Name**     | Kritika Aggarwal               |
| **Roll Number**   | 2310991878                     |
| **GitHub Profile**| https://github.com/kritika0519 |
| **Contribution**  | Created the JS-Free frontend using advanced CSS for styling, responsive layouts, and animations. |

---

### 🧑‍💻 Student 6

| Field             | Details                        |
|-------------------|--------------------------------|
| **Full Name**     | Nitasha                        |
| **Roll Number**   | 2310991917                     |
| **GitHub Profile**| https://github.com/nitasha1917 |
| **Contribution**  | Developed the vulnerable endpoints for SQLi, XSS, and IDOR demonstrations and drafted the final project PDF. |

---

## 📦 Submission Checklist

Before raising your Pull Request, confirm every item below:

- [ ] All 6 student blocks above are fully filled in
- [ ] Deployed URL is working and accessible
- [ ] Project code is inside `student_folder/grp6/src/`
- [ ] PDF report is included as `student_folder/grp6/report.pdf`
- [ ] Branch name follows format: `grp6-<project-name>`
- [ ] PR is targeting the `develop` branch — NOT `main`
- [ ] No `.env` files or secret keys are committed
- [ ] No other group's folder has been touched

---

## 📝 Project Description

>The **SecureWeb Vulnerability Lab** is an interactive web application built with Python and Flask, serving as an educational cybersecurity platform. It demonstrates common web vulnerabilities and robust defensive programming techniques. The application embraces a "No-JS" philosophy, relying entirely on advanced CSS to reduce client-side attack surfaces. It provides hands-on demonstrations of attacks like **SQL Injection (SQLi)**, **Cross-Site Scripting (XSS)**, and **Insecure Direct Object Reference (IDOR)**, alongside custom security mechanisms.
---

## 🔐 Security Concepts Implemented

>1. **Secure Authentication Flow**: Utilizes `bcrypt` for secure password hashing and salting. Uses **JSON Web Tokens (JWT)** for session management, stored securely in `HttpOnly` cookies to mitigate XSS session hijacking.
2. **Custom Password Strength Enforcement**: Validates passwords against strict complexity rules (uppercase, lowercase, numbers, special characters, and minimum length) and rejects common/weak dictionary passwords.
3. **Brute-Force Defense & Logging**: Monitors and logs all login attempts locally. Analyzes recent attempts to detect brute-force attacks and dynamically triggers security alerts.
4. **SQL Injection Prevention**: Uses parameterized queries (`?`) in a self-contained SQLite3 database to prevent SQL Injection in authenticated routes.
5. **XSS Mitigation & JS-Free Frontend**: Relies on standard Jinja2 syntax to escape user inputs natively, mitigating XSS vulnerabilities, and uses pure CSS for interactive UI and animations, eliminating JavaScript dependencies.
---

> ⚠️ **Reminder:** Only **one person** from the group raises the Pull Request.  
> The branch must be created from `develop` — never from `main`.  
> Branch name format: `grp6-your-project-name`

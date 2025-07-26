# 🧪 rak-wbg-test-framework

### ✅ End-to-End Automation Testing Framework for RAK-WBG Web Application

The `rak-wbg-test-framework` is a scalable and maintainable automation suite built using **Python**, **Playwright**, and **Pytest**, designed to validate the core functionality and workflows of the **RAK-WBG platform**. This framework provides rich reporting, modular test design, and CI/CD integration capabilities for robust quality assurance.

---

## 🔧 Features

- ✅ Page Object Model (POM) architecture
- ✅ Built on Playwright for modern web automation
- ✅ Supports Chromium, Firefox, and WebKit browsers
- ✅ Integrated with Allure for enhanced reporting
- ✅ Tagged test execution with `@pytest.mark`
- ✅ Environment-specific configuration
- ✅ Responsive layout, accessibility & edge case test coverage

---

## 📦 Project Structure

```

rak-wbg-test-framework/
│
├── pages/                  # Page Object Models for different modules
├── tests/                  # Pytest test files
├── utils/
│   ├── config.py           # Configuration for environment URLs and credentials
│   └── helpers.py          # Utility functions
├── reports/                # Allure report output
├── .env                    # Environment variables (optional)
├── requirements.txt        # Dependencies
├── pytest.ini              # Pytest settings
└── README.md               # You're here

````

---

## 🧪 Modules Covered

- 🔐 **Login** — Valid/invalid credential testing
- 📊 **Pipeline** — RM search, table validation, responsiveness
- 📁 **Portfolio** — Facility filtering, totals validation, negative scenarios
- 📌 **Task Board** — Card creation, edit, delete, move across stages
- 🧭 **Navigation** — MIR and Past Dues redirection
- 📝 **Account Planning** — Plan setup, approval flow, user access roles
- 🏢 **Companies** — Company listing, search, and profile view validation
- 💬 **Threads** — Thread creation, tagging, and comment history
- ❌ **Negative Tests** — Invalid dropdowns, missing values, edge input handling

---

## 🚀 Getting Started

### 🔗 Clone the Repository

```bash
git clone https://github.com/your-org/rak-wbg-test-framework.git
cd rak-wbg-test-framework
````

### 🛠 Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

> Ensure Python 3.9+ is installed and virtual environment is activated.

---

## 🧪 Running Tests

### Run All Tests (Headless)

```bash
pytest
```

### Run Specific Tag (e.g., smoke)

```bash
pytest -m smoke
```

### Run with Browser UI

```bash
pytest --headed
```

---

## 📊 Generating Allure Reports

### 1. Run Tests with Allure Output

```bash
pytest --alluredir=reports/
```

### 2. Serve the Report Locally

```bash
allure serve reports/
```

> 📌 To include **Environment** and **Executor** metadata in the report:

* Create an `environment.properties` file in `reports/`
* Create an `executor.json` file in `reports/`

Example:

```properties
Browser=Chromium
URL=https://rak-wbg.gamechange.dev
Environment=QA
```

```json
{
  "name": "GitHub Actions",
  "type": "CI",
  "url": "https://github.com/your-org/rak-wbg-test-framework/actions"
}
```

---

## 🧠 Tech Stack

| Tech        | Purpose                 |
| ----------- | ----------------------- |
| Python      | Core scripting language |
| Playwright  | Web automation engine   |
| Pytest      | Test framework          |
| Allure      | Reporting               |
| POM Pattern | Test architecture       |

---

## 🔄 CI/CD Integration

This framework is designed to easily integrate with:

* **GitHub Actions**
* **Jenkins**
* **GitLab CI**
* **Azure DevOps**

You can configure it to run nightly or trigger on pull requests to maintain product quality.

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch: `feature/account-planning-tests`
3. Commit changes: `git commit -m 'Added tests for Account Planning module'`
4. Push to your branch: `git push origin feature/account-planning-tests`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For questions, feature requests, or issues, feel free to [open an issue](https://github.com/your-org/rak-wbg-test-framework/issues) or contact the QA team.

---

🔁 **Happy Testing!**

```

---

Let me know if you'd like:
- a version with badge icons (e.g. build, coverage),
- a downloadable `.md` file,
- or additions like screenshots, coverage summary, or CI status examples.
```

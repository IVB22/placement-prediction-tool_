# FuturePath Enterprise (Java Console + Python ML Service) — JDBC Storage (SQLite)

This version keeps the core behavior the same:
- Java console collects input and calls Python backend at `POST /match-json`.

Change requested:
- **MongoDB history is replaced with JDBC storage** using **SQLite** inside the Java app.
- Java stores full **request JSON** (including full/trimmed `resume_text`) + **response JSON** + timestamp.

Python service remains the ML backend (no DB required).

## Run

### 1) Start Python backend
```bash
cd python_service
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Health: http://127.0.0.1:5000/health

### 2) Run Java console (JDBC / SQLite)
```bash
cd java_console
mvn -q -DskipTests package
java -jar target/tool.jar
```

SQLite DB file is created automatically at:
- `java_console/futurepath.db`

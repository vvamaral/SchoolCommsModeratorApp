# 🏫 SchoolCommsModeratorApp

**SchoolCommsModeratorApp** is a communication moderation assistant for school environments. It helps ensure that messages sent through school communication systems are grammatically correct and free from inappropriate or banned content.

## 📆 Project Structure

```
SchoolCommsModeratorApp/
├── app/
│   ├── languagetool/              # LanguageTool server and files
│   ├── services/
│   │   ├── grammar_checker.py     # Handles grammar/spell checking
│   │   └── moderation_service.py  # Handles moderation logic (e.g., banned words)
│   ├── utils/
│   │   └── __init__.py            # Utility functions (future use)
│   ├── config.py                  # Configuration values and constants
│   └── routes.py                  # API route definitions
├── .dockerignore                  # Files and folders to ignore in Docker build
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker multi-service orchestration
├── Dockerfile                     # Docker build instructions
├── main.py                        # Entry point for Flask app
├── requirements.txt               # Python dependencies (Cloud)
├── requirements-local.txt         # Python dependencies (Local dev - Windows)
└── run_services.sh                # Shell script to start LanguageTool + Flask
```

## 🚀 Features

- ✅ REST API with Flask
- 📚 Grammar and spell checking using [LanguageTool](https://languagetool.org/)
- ❌ Content moderation for banned or inappropriate words
- 🟣 Fully containerized with Docker and ready for deployment on **Google Cloud Run**

## 🔠 API Endpoints

### `GET /`

Returns a simple health check message.

### `POST /moderar`

Validates a text input to detect banned words.

- **Body Example:**

```json
{
  "texto": "Esse menino é um idiota"
}
```

- **Response Example:**

```json
{
  "status": "REJEITADO",
  "motivo": "Palavra(s) proibida(s) detectada(s): idiota."
}
```

### `POST /analyze-text`

Returns suggestions from the grammar/spell checker for a given text.

- **Body Example:**

```json
{
  "texto": "Eu vô para a escola amanha."
}
```

- **Response Example:**

```json
{
  "matches": [
    {
      "message": "Possible spelling mistake found.",
      "offset": 3,
      "length": 2,
      "replacements": ["vou"]
    },
    ...
  ]
}
```

## 🧪 Local Development (Windows)

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements-local.txt
```

### 3. Run Flask manually

Start LanguageTool in a separate terminal:

```bash
java -cp "app/languagetool/LanguageTool-6.6/*" org.languagetool.server.HTTPServer --port 8081
```

Then run Flask:

```bash
python main.py
```

## 🟣 Docker & Cloud Deployment

### Build and push Docker image

```bash
docker build -t LOCATION-docker.pkg.dev/PROJECT_ID/school-comms-repo/schoolcommsmoderator:latest .
docker push LOCATION-docker.pkg.dev/PROJECT_ID/school-comms-repo/schoolcommsmoderator:latest
```

### Deploy to Google Cloud Run

```bash
gcloud run deploy school-comms-moderator \
  --image LOCATION-docker.pkg.dev/PROJECT_ID/school-comms-repo/schoolcommsmoderator:latest \
  --platform managed \
  --region LOCATION \
  --allow-unauthenticated \
  --port 8080 \
  --timeout=360s
```

## 📒 Dependencies

- Python 3.9+
- Flask 3.1.1
- Flask-CORS
- Requests
- Unidecode (for accent-insensitive comparison)
- LanguageTool 6.6 (Java-based)
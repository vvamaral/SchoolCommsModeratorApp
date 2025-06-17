#!/bin/bash
set -e

echo "Starting services..."
echo "PYTHON_PATH: /app/venv/bin/python3"
echo "JAVA_PATH: $(which java)"

LT_CLASSPATH=$(find /app/languagetool -name "*.jar" | tr '\n' ':')

echo "Starting LanguageTool server..."
java -cp "$LT_CLASSPATH" org.languagetool.server.HTTPServer --port 8081 &

LT_PID=$!

MAX_RETRIES=30
RETRY_INTERVAL=1
LT_URL="http://localhost:8081/v2/languages"

echo "Waiting for LanguageTool to start..."
for i in $(seq 1 $MAX_RETRIES); do
  if curl -s -f --connect-timeout 5 "$LT_URL" > /dev/null; then
    echo "LanguageTool started successfully!"
    break
  fi
  echo "LanguageTool not ready yet, retrying in $RETRY_INTERVAL second(s)... ($i/$MAX_RETRIES)"
  sleep $RETRY_INTERVAL
done

if ! curl -s -f --connect-timeout 5 "$LT_URL" > /dev/null; then
  echo "ERROR: LanguageTool failed to start within the expected time."
  exit 1
fi

echo "LanguageTool started. Starting Flask app..."
exec /app/venv/bin/python3 -m flask run --host=0.0.0.0 --port=8080
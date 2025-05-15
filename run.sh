#!/bin/bash

cd "$(dirname "$0")"
export FLASK_APP=app.py

# Start Flask in the background and save PID
flask run > flask.log 2>&1 &
FLASK_PID=$!

# Wait for Flask to start
echo "Waiting for Flask to start..."
until curl -s http://localhost:5000 > /dev/null; do
    sleep 0.5
done
echo "Flask is up!"

# Create a temp Chrome user profile
TMP_PROFILE=$(mktemp -d)

# Launch Chrome in app mode with all prompts and updates disabled
google-chrome \
  --user-data-dir="$TMP_PROFILE" \
  --app=http://localhost:5000 \
  --no-first-run \
  --no-default-browser-check \
  --disable-default-apps \
  --disable-extensions \
  --disable-component-update \
  --disable-background-networking \
  --disable-sync \
  --metrics-recording-only \
  &
CHROME_PID=$!

# Wait for Chrome to close
wait $CHROME_PID

# Kill Flask
kill $FLASK_PID

# Clean up Chrome profile
rm -rf "$TMP_PROFILE"

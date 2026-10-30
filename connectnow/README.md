# ConnectNow
Firebase Realtime Database chat with anonymous sign-in, room selection and latest-100-message listener.
## Setup
Register a Firebase Web app; enable Authentication → Anonymous and Realtime Database; replace the config placeholders in `index.html`. Serve locally with `python -m http.server 8000`.
## Security
Never use public read/write rules. Require authentication, validate message length/shape, rate-limit writes, and add moderation/reporting before launch. The Firebase web config is public by design; database rules protect data.
# Malkify Tasks

Flutter task manager with Firebase Authentication and Cloud Firestore.

## Configure Firebase
1. Create a Firebase project and register a Flutter app for each target platform.
2. Enable Email/Password in Firebase Authentication.
3. Create a Cloud Firestore database.
4. Find the app's Firebase config values in Firebase Console → Project settings.
5. Run the app with these compile-time values:

```bash
flutter pub get
flutter run \
  --dart-define=FIREBASE_API_KEY=YOUR_API_KEY \
  --dart-define=FIREBASE_APP_ID=YOUR_APP_ID \
  --dart-define=FIREBASE_MESSAGING_SENDER_ID=YOUR_SENDER_ID \
  --dart-define=FIREBASE_PROJECT_ID=YOUR_PROJECT_ID \
  --dart-define=FIREBASE_AUTH_DOMAIN=YOUR_PROJECT.firebaseapp.com \
  --dart-define=FIREBASE_STORAGE_BUCKET=YOUR_PROJECT.firebasestorage.app
```

The app requires valid Firebase configuration before launch. Configure Firestore security rules so each signed-in user can only read and write their own `users/{uid}/tasks` collection. Do not use open test-mode rules in production.

# Task Manager — Flutter + Firebase

A task list starter with Firebase email/password authentication and Cloud Firestore.

Setup: create a Firebase project, register the Flutter app, run flutterfire configure, enable Email/Password Authentication, create Firestore, then run flutter pub get and flutter run. Firebase-generated firebase_options.dart is intentionally excluded from Git. Apply Firestore security rules so users can access only their own tasks.
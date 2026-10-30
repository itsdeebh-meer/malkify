# Malkify Movies

Flutter movie discovery app powered by TMDB.

## Features
- Popular movie discovery and title search
- Movie poster, synopsis and rating detail sheet
- Local saved-movie list with a favorites filter
- Responsive Material 3 dark interface

## Run
1. Install Flutter stable.
2. Create a TMDB API Read Access Token in your TMDB account.
3. From this folder run:

```bash
flutter pub get
flutter run --dart-define=TMDB_TOKEN=YOUR_TMDB_READ_ACCESS_TOKEN
```

The token is injected at build time and is not committed to this repository. TMDB network access is required. Saved movies are stored locally on the device; they are not synced across devices.

# Malkify — Developer Portfolio

A collection of practical projects built with web technologies, Flutter, Firebase, Python and public APIs.

## Projects

| Project | Stack | Description |
|---|---|---|
| [Weather App](./weather-app) | HTML, CSS, JavaScript | City weather lookup; OpenWeatherMap key required. |
| [Movie Platform](./movie-platform) | Flutter, Dart, TMDB | Movie discovery and local bookmarks; configure a TMDB token. |
| [AI Chatbot](./ai-chatbot) | Python, Flask, Gemini | Basic Gemini-powered chatbot; configure a server-side API key. |
| [Task Manager](./task-manager) | Flutter, Dart, Firebase | Task CRUD with Firebase Authentication and Firestore setup. |
| [ShopVerse](./shopverse) | HTML, CSS, JavaScript | Product catalogue, search and persistent demo cart. |
| [DevPortfolio](./devportfolio) | HTML, CSS, JavaScript | Responsive developer portfolio and email contact link. |
| [SmartCV](./smartcv) | Python, Flask | Resume builder with print-to-PDF workflow. |
| [ExpenseX](./expensex) | Flutter, Dart | Local expense tracker with persistent entries. |
| [ConnectNow](./connectnow) | HTML, JavaScript, Firebase | Realtime room chat; Firebase setup and secure rules required. |
| [JobFinder](./jobfinder) | HTML, CSS, JavaScript | Sample job listings, filters and local application tracker. |
| [Linkify](./linkify) | Python, Flask, SQLite | URL shortener and redirect click counter. |
| [LearnHub](./learnhub) | HTML, CSS, JavaScript | Beginner lessons, quizzes and local progress tracking. |
| [DeniAI Studio](./deniai-studio) | Python, Flask, Gemini | Server-side Gemini prompt assistant; API key required. |
| [MediBook](./medibook) | Python, Flask, SQLite | Local appointment-request demo; not a real healthcare service. |
| [DevTrack](./devtrack) | React, Node.js, Express, PostgreSQL, Prisma | Project management workspace with JWT auth, projects, Kanban tasks and comments. |
| [StockPilot](./stockpilot) | React, Node.js, Express, PostgreSQL, Prisma | Inventory catalogue, stock adjustment and low-stock business rules. |
| [HelpDesk Pro](./helpdesk-pro) | React, Node.js, Express, Socket.IO, PostgreSQL | Support ticket API with realtime ticket and message events. |
| [SkillSphere](./skillsphere) | React, Node.js, Express, PostgreSQL, Prisma, JWT | User registration/login, course catalogue and enrollment API. |
| [UptimeX](./uptimex) | React, Node.js, Express, PostgreSQL, Prisma | HTTP endpoint checks, latency history and manual health checks. |

## Getting started

Open each project folder's README for its setup instructions. Web projects require Node.js and their listed packages. Flutter projects require the Flutter SDK. Python projects require Python and their listed packages.

## Important status and security notes

These projects are learning-oriented MVPs, not audited production services. External integrations require your own API keys and Firebase configuration. Never commit secrets. Sample job listings and sample products are not live commercial data. ShopVerse does not process payments; JobFinder does not submit job applications; MediBook does not contact clinics and must not be used for sensitive health information. ConnectNow must have secure Firebase database rules before use.

The four new projects include starter APIs, Prisma data models and React dashboards. Configure PostgreSQL and run migrations locally. HelpDesk Pro broadcasts realtime events, while its dashboard remains a starter interface. SkillSphere includes JWT registration/login and course/enrollment endpoints, but instructor provisioning and lesson completion UX remain to be built. UptimeX includes manual checks; a durable production scheduler and comprehensive SSRF defenses are not included. StockPilot's dashboard is a starter CRUD view; purchase/sale movement endpoints are API-first.

Run each project's documented checks locally before relying on it. No claim is made that every app has been built or runtime-tested in this repository environment.

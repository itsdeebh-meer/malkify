# Deployment guide

## Static web apps and portfolio

The GitHub Actions workflow publishes the repository root to GitHub Pages after CI passes. In GitHub, open Settings → Pages and set Build and deployment → Source to GitHub Actions. The deployment job will then provide the canonical live URL in its deployment summary.

Static apps included: ShopVerse, DevPortfolio, JobFinder and LearnHub. ConnectNow is also static-hostable, but it requires Firebase web configuration and secure Realtime Database rules before its chat functions can connect.

## Flask services

A Render Blueprint manifest is included at the repository root. To create the four backend services:

1. Sign in to Render and choose New → Blueprint.
2. Connect this GitHub repository and select the main branch.
3. Review the four services in render.yaml and deploy the Blueprint.
4. Add your Gemini API key as the GEMINI_API_KEY secret for DeniAI Studio in the Render dashboard.

The manifest provisions SmartCV, Linkify, DeniAI Studio and MediBook. Render creates their public service URLs after deployment.

Storage note: the free-tier manifest uses temporary filesystem paths for Linkify and MediBook databases. Data can be lost when a service restarts or redeploys. For persistent production data, attach persistent storage on a paid plan or migrate those apps to a managed database before using them for real users.

## Flutter apps

ExpenseX, Malkify Movies and Malkify Tasks are Flutter applications, not ordinary static HTML sites. Build and deploy them as Android/iOS apps or compile them for web with Flutter. Malkify Movies needs a TMDB Read Access Token; Malkify Tasks needs Firebase project configuration. Follow each app's README.

## Secrets and safety

Never commit API keys, Firebase service-account files, production passwords or .env files. Use repository/hosting secret settings. Do not use demo Firebase database rules in production.

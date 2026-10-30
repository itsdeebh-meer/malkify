# HelpDesk Pro

Professional full-stack portfolio MVP for support tickets and real-time updates.

## Stack
React, Vite, Node.js, Express, PostgreSQL, Prisma, Socket.IO.

## Run locally
1. Install Node.js 20+ and PostgreSQL.
2. `cd server && npm install`.
3. Copy `.env.example` to `.env` and configure DATABASE_URL.
4. `npx prisma generate && npx prisma migrate dev --name init`.
5. `npm run dev` in server.
6. In client run `npm install`, copy .env.example to .env, then `npm run dev`.

API port 4002; frontend port 5173. Check API at /api/health.

## Production hardening
Socket.IO events broadcast ticket creation, updates and messages. Add user roles, ticket access controls, rate limiting and message history UI.

This is a portfolio MVP, not a production-hardened service. Test locally before deployment.
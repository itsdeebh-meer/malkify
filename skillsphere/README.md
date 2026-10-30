# SkillSphere

Professional full-stack portfolio MVP for learner accounts, courses and enrollment.

## Stack
React, Vite, Node.js, Express, PostgreSQL, Prisma, JWT and bcrypt.

## Run locally
1. Install Node.js 20+ and PostgreSQL.
2. `cd server && npm install`.
3. Copy `.env.example` to `.env` and configure DATABASE_URL and JWT_SECRET (32+ chars).
4. `npx prisma generate && npx prisma migrate dev --name init`.
5. `npm run dev` in server.
6. In client run `npm install`, copy .env.example to .env, then `npm run dev`.

API port 4003; frontend port 5173. Check API at /api/health.

## Production hardening
JWT and bcrypt registration/login are included. Add instructor provisioning, email verification, password reset, lesson completion and quiz workflows.

This is a portfolio MVP, not a production-hardened service. Test locally before deployment.
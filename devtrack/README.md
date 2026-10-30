# DevTrack

A full-stack project management workspace built with React, Node.js, Express, Prisma and PostgreSQL.

## Features
- Account registration and login (bcrypt + JWT)
- Project creation, listing and deletion
- Kanban task board: To do, In progress, Review, Done
- Task priorities, due dates and task assignment to project members
- Task comments
- Dashboard metrics and upcoming deadlines
- Responsive React interface

## Stack
React + Vite · Node.js + Express · PostgreSQL · Prisma ORM

## Run locally
Requirements: Node.js 20+, PostgreSQL 14+.

### Backend
```bash
cd devtrack/server
npm install
cp .env.example .env
# Edit DATABASE_URL and JWT_SECRET in .env
npx prisma generate
npx prisma migrate dev --name init
npm run seed
npm run dev
```
API: http://localhost:5000

Demo login after seeding:
- Email: `demo@devtrack.local`
- Password: `DevTrack123!`

### Frontend
In a second terminal:
```bash
cd devtrack/client
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173.

## Environment
Backend `server/.env`:
```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/devtrack?schema=public"
JWT_SECRET="replace-with-a-random-secret-of-at-least-32-characters"
PORT=5000
CLIENT_URL="http://localhost:5173"
NODE_ENV="development"
```
Frontend `client/.env`:
```env
VITE_API_URL=http://localhost:5000/api
```

## API
| Method | Route | Purpose |
|---|---|---|
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Current user |
| GET, POST | /api/projects | List/create projects |
| GET, DELETE | /api/projects/:id | Project detail/delete |
| GET, POST | /api/projects/:id/tasks | List/create tasks |
| PATCH, DELETE | /api/tasks/:id | Update/delete task |
| GET, POST | /api/tasks/:id/comments | Task comments |
| GET | /api/dashboard | Workspace metrics |
| GET | /api/health | Health check |

Authenticated endpoints require `Authorization: Bearer <token>`.

## Security
- Never commit `.env` files or real credentials.
- Use a unique, long JWT secret and HTTPS in production.
- Restrict database access and configure backups.
- Add rate limiting, email verification, password reset and audit logs before production deployment.
- Seed credentials are for local demonstration only.
- This is a portfolio MVP and has not undergone a security audit.

## License
MIT

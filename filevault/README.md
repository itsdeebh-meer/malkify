# FileVault

Premium dark SaaS cloud file manager for the Malkify portfolio. Built with React + TypeScript + Vite and Supabase Auth/Postgres/Storage.

## Features
- Email/password authentication
- Private Supabase Storage bucket with owner-scoped RLS
- Multi-file uploads (up to 500 MB per object; resumable uploads can be added for larger objects)
- Folder navigation and creation
- Search, favorites, shared files and trash
- Signed download/share URLs
- Responsive premium dark UI
- Storage usage indicator
- Production-oriented RLS SQL and CI build verification

## Local setup
1. Create a Supabase project.
2. Open **SQL Editor** and run `supabase/schema.sql`.
3. Copy `.env.example` to `.env.local` and set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
4. From this directory run `npm install` then `npm run dev`.

Never put a Supabase service-role key in Vite environment variables. The browser app only uses the public anon key; authorization is enforced by Supabase RLS.

## Deployment
Recommended: Vercel or any static host that supports Vite.
- Build command: `npm run build`
- Output directory: `dist`
- Environment variables: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`
- Configure your production site URL under Supabase Authentication > URL Configuration.

## Security model
The `filevault` bucket is private. Every object path starts with the authenticated user's UUID, and Storage policies only permit that user to select/insert/update/delete objects in their own prefix. Database rows are similarly protected by owner-based RLS. File sharing uses expiring signed URLs rather than public bucket URLs.

Supabase recommends standard uploads for smaller files and resumable/TUS uploads for files above roughly 6 MB when reliability matters; this first production release uses the simple SDK upload path and caps objects at 500 MB. See Supabase's Storage documentation before enabling very large uploads.

## Verification
Run `npm run build` locally or rely on the GitHub Actions workflow in `.github/workflows/filevault.yml`.

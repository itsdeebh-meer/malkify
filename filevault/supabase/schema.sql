-- FileVault Supabase setup. Run once in Supabase SQL Editor.
create extension if not exists pgcrypto;

create table if not exists public.folders (
  id uuid primary key default gen_random_uuid(), owner_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 1 and 120), parent_id uuid references public.folders(id) on delete cascade,
  created_at timestamptz not null default now(), deleted_at timestamptz
);
create index if not exists folders_owner_parent_idx on public.folders(owner_id,parent_id);

create table if not exists public.files (
  id uuid primary key default gen_random_uuid(), owner_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 1 and 255), path text not null unique,
  size bigint not null default 0 check (size >= 0), mime_type text not null default 'application/octet-stream',
  folder_id uuid references public.folders(id) on delete set null, is_favorite boolean not null default false,
  shared_at timestamptz, created_at timestamptz not null default now(), deleted_at timestamptz
);
create index if not exists files_owner_folder_idx on public.files(owner_id,folder_id);
create index if not exists files_owner_deleted_idx on public.files(owner_id,deleted_at);

alter table public.folders enable row level security;
alter table public.files enable row level security;

drop policy if exists folders_owner_all on public.folders;
create policy folders_owner_all on public.folders for all using (owner_id=auth.uid()) with check (owner_id=auth.uid());
drop policy if exists files_owner_all on public.files;
create policy files_owner_all on public.files for all using (owner_id=auth.uid()) with check (owner_id=auth.uid());

insert into storage.buckets (id,name,public,file_size_limit)
values ('filevault','filevault',false,524288000)
on conflict (id) do update set public=false,file_size_limit=524288000;

drop policy if exists filevault_select on storage.objects;
create policy filevault_select on storage.objects for select to authenticated using (bucket_id='filevault' and (storage.foldername(name))[1]=auth.uid()::text);
drop policy if exists filevault_insert on storage.objects;
create policy filevault_insert on storage.objects for insert to authenticated with check (bucket_id='filevault' and (storage.foldername(name))[1]=auth.uid()::text);
drop policy if exists filevault_update on storage.objects;
create policy filevault_update on storage.objects for update to authenticated using (bucket_id='filevault' and (storage.foldername(name))[1]=auth.uid()::text) with check (bucket_id='filevault' and (storage.foldername(name))[1]=auth.uid()::text);
drop policy if exists filevault_delete on storage.objects;
create policy filevault_delete on storage.objects for delete to authenticated using (bucket_id='filevault' and (storage.foldername(name))[1]=auth.uid()::text);

-- Optional cleanup helper for scheduled jobs.
create or replace function public.purge_old_trash() returns void language sql security definer set search_path=public as $$
  delete from public.files where deleted_at < now() - interval '30 days';
$$;

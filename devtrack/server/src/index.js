import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { z } from 'zod';

const prisma = new PrismaClient();
const app = express();

if (!process.env.JWT_SECRET || process.env.JWT_SECRET.length < 32) {
  throw new Error('JWT_SECRET must be configured with at least 32 characters.');
}
app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:5173' }));
app.use(express.json({ limit: '1mb' }));

const asyncRoute = fn => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
const auth = asyncRoute(async (req, res, next) => {
  const token = req.headers.authorization?.startsWith('Bearer ') ? req.headers.authorization.slice(7) : null;
  if (!token) return res.status(401).json({ message: 'Authentication required.' });
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await prisma.user.findUnique({ where: { id: payload.sub }, select: { id: true, name: true, email: true } });
    if (!req.user) return res.status(401).json({ message: 'Account not found.' });
    next();
  } catch { return res.status(401).json({ message: 'Invalid or expired token.' }); }
});
const issueToken = user => jwt.sign({ sub: user.id }, process.env.JWT_SECRET, { expiresIn: '7d' });
const projectAccess = (projectId, userId) => prisma.project.findFirst({ where: { id: projectId, members: { some: { userId } } } });
const taskAccess = (taskId, userId) => prisma.task.findFirst({ where: { id: taskId, project: { members: { some: { userId } } } } });

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

app.post('/api/auth/register', asyncRoute(async (req, res) => {
  const parsed = z.object({ name: z.string().trim().min(2).max(60), email: z.string().email().max(120), password: z.string().min(8).max(72) }).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: parsed.error.issues[0].message });
  const email = parsed.data.email.toLowerCase();
  if (await prisma.user.findUnique({ where: { email } })) return res.status(409).json({ message: 'Email already registered.' });
  const passwordHash = await bcrypt.hash(parsed.data.password, 12);
  const user = await prisma.user.create({ data: { name: parsed.data.name, email, passwordHash }, select: { id: true, name: true, email: true } });
  res.status(201).json({ user, token: issueToken(user) });
}));

app.post('/api/auth/login', asyncRoute(async (req, res) => {
  const parsed = z.object({ email: z.string().email(), password: z.string().min(1) }).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: 'Enter a valid email and password.' });
  const user = await prisma.user.findUnique({ where: { email: parsed.data.email.toLowerCase() } });
  if (!user || !(await bcrypt.compare(parsed.data.password, user.passwordHash))) return res.status(401).json({ message: 'Incorrect email or password.' });
  const safeUser = { id: user.id, name: user.name, email: user.email };
  res.json({ user: safeUser, token: issueToken(safeUser) });
}));

app.get('/api/auth/me', auth, (req, res) => res.json({ user: req.user }));

app.use('/api', auth);

app.get('/api/projects', asyncRoute(async (req, res) => {
  const projects = await prisma.project.findMany({
    where: { members: { some: { userId: req.user.id } } },
    include: { _count: { select: { tasks: true, members: true } }, tasks: { select: { status: true } } },
    orderBy: { updatedAt: 'desc' }
  });
  res.json({ projects });
}));

app.post('/api/projects', asyncRoute(async (req, res) => {
  const parsed = z.object({ name: z.string().trim().min(2).max(80), description: z.string().max(500).optional().default(''), color: z.string().regex(/^#[0-9a-fA-F]{6}$/).optional().default('#7c6cff') }).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: parsed.error.issues[0].message });
  const project = await prisma.project.create({ data: { ...parsed.data, ownerId: req.user.id, members: { create: { userId: req.user.id, role: 'OWNER' } } }, include: { _count: { select: { tasks: true, members: true } } } });
  res.status(201).json({ project });
}));

app.get('/api/projects/:id', asyncRoute(async (req, res) => {
  const project = await projectAccess(req.params.id, req.user.id);
  if (!project) return res.status(404).json({ message: 'Project not found.' });
  const result = await prisma.project.findUnique({ where: { id: project.id }, include: {
    members: { include: { user: { select: { id: true, name: true, email: true } } } },
    tasks: { include: { assignee: { select: { id: true, name: true } }, _count: { select: { comments: true } } }, orderBy: { updatedAt: 'desc' } }
  }});
  res.json({ project: result });
}));

app.delete('/api/projects/:id', asyncRoute(async (req, res) => {
  const project = await prisma.project.findFirst({ where: { id: req.params.id, ownerId: req.user.id } });
  if (!project) return res.status(404).json({ message: 'Project not found or you are not the owner.' });
  await prisma.project.delete({ where: { id: project.id } });
  res.json({ message: 'Project deleted.' });
}));

app.get('/api/projects/:id/tasks', asyncRoute(async (req, res) => {
  const project = await projectAccess(req.params.id, req.user.id);
  if (!project) return res.status(404).json({ message: 'Project not found.' });
  const tasks = await prisma.task.findMany({ where: { projectId: project.id }, include: { assignee: { select: { id: true, name: true } }, _count: { select: { comments: true } } }, orderBy: { updatedAt: 'desc' } });
  res.json({ tasks });
}));

app.post('/api/projects/:id/tasks', asyncRoute(async (req, res) => {
  const project = await projectAccess(req.params.id, req.user.id);
  if (!project) return res.status(404).json({ message: 'Project not found.' });
  const parsed = z.object({ title: z.string().trim().min(2).max(120), description: z.string().max(1000).optional().default(''), priority: z.enum(['LOW','MEDIUM','HIGH','URGENT']).optional().default('MEDIUM'), dueDate: z.string().datetime().nullable().optional() }).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: parsed.error.issues[0].message });
  const task = await prisma.task.create({ data: { ...parsed.data, dueDate: parsed.data.dueDate ? new Date(parsed.data.dueDate) : null, projectId: project.id }, include: { assignee: { select: { id: true, name: true } }, _count: { select: { comments: true } } } });
  res.status(201).json({ task });
}));

app.patch('/api/tasks/:id', asyncRoute(async (req, res) => {
  const task = await taskAccess(req.params.id, req.user.id);
  if (!task) return res.status(404).json({ message: 'Task not found.' });
  const parsed = z.object({
    title: z.string().trim().min(2).max(120).optional(),
    description: z.string().max(1000).optional(),
    status: z.enum(['TODO','IN_PROGRESS','REVIEW','DONE']).optional(),
    priority: z.enum(['LOW','MEDIUM','HIGH','URGENT']).optional(),
    dueDate: z.string().datetime().nullable().optional()
  }).refine(v => Object.keys(v).length > 0).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: 'Invalid task update.' });
  const data = { ...parsed.data };
  if (data.dueDate !== undefined) data.dueDate = data.dueDate ? new Date(data.dueDate) : null;
  const updated = await prisma.task.update({ where: { id: task.id }, data, include: { assignee: { select: { id: true, name: true } }, _count: { select: { comments: true } } } });
  res.json({ task: updated });
}));

app.delete('/api/tasks/:id', asyncRoute(async (req, res) => {
  const task = await taskAccess(req.params.id, req.user.id);
  if (!task) return res.status(404).json({ message: 'Task not found.' });
  await prisma.task.delete({ where: { id: task.id } });
  res.json({ message: 'Task deleted.' });
}));

app.get('/api/tasks/:id/comments', asyncRoute(async (req, res) => {
  const task = await taskAccess(req.params.id, req.user.id);
  if (!task) return res.status(404).json({ message: 'Task not found.' });
  const comments = await prisma.comment.findMany({ where: { taskId: task.id }, include: { author: { select: { id: true, name: true } } }, orderBy: { createdAt: 'asc' } });
  res.json({ comments });
}));

app.post('/api/tasks/:id/comments', asyncRoute(async (req, res) => {
  const task = await taskAccess(req.params.id, req.user.id);
  if (!task) return res.status(404).json({ message: 'Task not found.' });
  const parsed = z.object({ body: z.string().trim().min(1).max(1000) }).safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ message: 'Comment cannot be empty.' });
  const comment = await prisma.comment.create({ data: { body: parsed.data.body, taskId: task.id, authorId: req.user.id }, include: { author: { select: { id: true, name: true } } } });
  res.status(201).json({ comment });
}));

app.get('/api/dashboard', asyncRoute(async (req, res) => {
  const where = { project: { members: { some: { userId: req.user.id } } } };
  const [projects, groups, dueSoon] = await Promise.all([
    prisma.project.count({ where: { members: { some: { userId: req.user.id } } } }),
    prisma.task.groupBy({ by: ['status'], where, _count: { _all: true } }),
    prisma.task.findMany({ where: { ...where, dueDate: { gte: new Date(), lte: new Date(Date.now()+7*86400000) }, status: { not: 'DONE' } }, include: { project: { select: { name: true } } }, orderBy: { dueDate: 'asc' }, take: 5 })
  ]);
  const counts = Object.fromEntries(['TODO','IN_PROGRESS','REVIEW','DONE'].map(s => [s,0]));
  groups.forEach(g => counts[g.status] = g._count._all);
  res.json({ stats: { projects, ...counts, totalTasks: Object.values(counts).reduce((a,b)=>a+b,0) }, dueSoon });
}));

app.use((req,res) => res.status(404).json({ message: 'Route not found.' }));
app.use((err,req,res,next) => {
  console.error(err);
  if (err.code === 'P2002') return res.status(409).json({ message: 'That value already exists.' });
  res.status(500).json({ message: 'Internal server error.' });
});

const port = Number(process.env.PORT) || 5000;
app.listen(port, () => console.log(`DevTrack API running on http://localhost:${port}`));

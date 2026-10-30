import 'dotenv/config';
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const passwordHash = await bcrypt.hash('DevTrack123!', 12);
  const user = await prisma.user.upsert({
    where: { email: 'demo@devtrack.local' },
    update: {},
    create: { name: 'Demo User', email: 'demo@devtrack.local', passwordHash }
  });

  const existing = await prisma.project.findFirst({ where: { ownerId: user.id, name: 'Website Redesign' } });
  if (existing) return console.log('Demo workspace already exists.');

  await prisma.project.create({
    data: {
      name: 'Website Redesign',
      description: 'Plan and deliver the next version of our product website.',
      ownerId: user.id,
      color: '#8b7cff',
      members: { create: { userId: user.id, role: 'OWNER' } },
      tasks: { create: [
        { title: 'Create design system', status: 'DONE', priority: 'HIGH', assigneeId: user.id },
        { title: 'Build dashboard layout', status: 'IN_PROGRESS', priority: 'URGENT', assigneeId: user.id },
        { title: 'Review mobile experience', status: 'REVIEW', priority: 'MEDIUM' },
        { title: 'Write launch checklist', status: 'TODO', priority: 'LOW' }
      ]}
    }
  });
  console.log('Demo account: demo@devtrack.local / DevTrack123!');
}

main().catch(e => { console.error(e); process.exit(1); }).finally(() => prisma.$disconnect());

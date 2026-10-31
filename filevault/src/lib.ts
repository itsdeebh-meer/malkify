import { createClient } from '@supabase/supabase-js';
export const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);
export const BUCKET = 'filevault';
export const formatBytes = (bytes:number) => { if (!bytes) return '0 B'; const u=['B','KB','MB','GB','TB']; const i=Math.floor(Math.log(bytes)/Math.log(1024)); return `${(bytes/Math.pow(1024,i)).toFixed(i?1:0)} ${u[i]}`; };
export const fileIcon = (type:string) => type.startsWith('image/')?'image':type.startsWith('video/')?'video':type.includes('pdf')?'pdf':type.includes('zip')||type.includes('rar')?'archive':type.includes('spreadsheet')||type.includes('excel')?'sheet':type.includes('word')?'doc':'file';

import Dexie from 'dexie';

const db = new Dexie('zoomail');
db.version(1).stores({
    messages: `id, title, content, html, sender, writer, created_at, updated_at, is_bookmarked`
});

export default db;

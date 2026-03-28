import sqlite3
import json
import datetime
import os
import threading
from pathlib import Path

# Dynamic path: dùng AOS_ROOT env var hoặc tự tính từ vị trí file này
_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
DB_PATH = os.path.join(_AOS_ROOT, "brain", "shared-context", "event_bus.db")

class AgentBus:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=True)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                picked_by TEXT
            )
        ''')
        self.conn.commit()

    def publish(self, topic, payload_dict):
        """Bắn tín hiệu vào Bus. payload là Dict."""
        payload_str = json.dumps(payload_dict, ensure_ascii=False)
        with self._lock:
            self.cursor.execute(
                "INSERT INTO events (topic, payload) VALUES (?, ?)",
                (topic, payload_str)
            )
            self.conn.commit()
            return self.cursor.lastrowid

    def poll(self, topics, agent_id="unknown"):
        """Agent quét Bus xem có việc cho mình không (chỉ lấy PENDING)."""
        placeholders = ','.join('?' * len(topics))
        query = f"SELECT id, topic, payload FROM events WHERE status='PENDING' AND topic IN ({placeholders}) ORDER BY created_at ASC"

        with self._lock:
            self.cursor.execute(query, topics)
            rows = self.cursor.fetchall()

            events = []
            for row in rows:
                event_id, topic, payload_str = row
                self.cursor.execute("UPDATE events SET status='PROCESSING', picked_by=? WHERE id=?", (agent_id, event_id))
                events.append({
                    "id": event_id,
                    "topic": topic,
                    "payload": json.loads(payload_str)
                })
            self.conn.commit()
        return events

    def mark_completed(self, event_id):
        with self._lock:
            self.cursor.execute("UPDATE events SET status='COMPLETED' WHERE id=?", (event_id,))
            self.conn.commit()

    def mark_failed(self, event_id):
        with self._lock:
            self.cursor.execute("UPDATE events SET status='FAILED' WHERE id=?", (event_id,))
            self.conn.commit()

    def get_pending_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM events WHERE status='PENDING'")
        return self.cursor.fetchone()[0]

    def clear_completed(self):
        with self._lock:
            self.cursor.execute("DELETE FROM events WHERE status='COMPLETED'")
            self.conn.commit()

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    bus = AgentBus()

    if action == "publish":
        topic = sys.argv[2]
        payload = sys.argv[3]
        eid = bus.publish(topic, {"task": payload})
        print(f"[PUB] Gửi thành công! EventID={eid}")

    elif action == "status":
        cnt = bus.get_pending_count()
        print(f"[STATUS] Task Bus hiện tại: {cnt} PENDING")
        bus.cursor.execute("SELECT id, topic, status, picked_by FROM events ORDER BY id DESC LIMIT 5")
        for r in bus.cursor.fetchall():
            print(f"  ID:{r[0]:03d} | Topic:{r[1]:<15} | Status:{r[2]:<10} | Agent:{r[3]}")

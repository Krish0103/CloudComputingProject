import datetime
import os

LOG_FILE = 'logs.txt'

def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write('# Login activity log\n')

def format_log_line(username: str, success: bool, reason: str) -> str:
    timestamp = datetime.datetime.now().isoformat()
    status = 'SUCCESS' if success else 'FAILURE'
    # Removing any newlines in username or reason just to keep log intact
    safe_username = username.replace('|', '').replace('\n', '')
    safe_reason = reason.replace('|', '').replace('\n', '')
    return f'{timestamp} | {safe_username} | {status} | {safe_reason}\n'

def record_login_attempt(username: str, success: bool, reason: str):
    ensure_log_file()
    line = format_log_line(username, success, reason)
    with open(LOG_FILE, 'a') as f:
        f.write(line)
    return line

def read_logs() -> list:
    ensure_log_file()
    with open(LOG_FILE, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

def parse_log_line(line: str) -> dict:
    parts = [part.strip() for part in line.split('|')]
    if len(parts) >= 4:
        return {
            'timestamp': datetime.datetime.fromisoformat(parts[0]),
            'username': parts[1],
            'status': parts[2],
            'reason': parts[3]
        }
    return None

def recent_failures(username: str, limit: int = 5) -> list:
    logs = read_logs()
    failures = []
    for line in reversed(logs):
        entry = parse_log_line(line)
        if entry and entry['username'] == username and entry['status'] == 'FAILURE':
            failures.append(entry)
            if len(failures) >= limit:
                break
    return failures

def is_brute_force(username: str, threshold: int = 3, window_minutes: int = 10) -> bool:
    failures = recent_failures(username, threshold)
    if len(failures) < threshold:
        return False
    earliest = failures[-1]['timestamp']
    latest = failures[0]['timestamp']
    delta = latest - earliest
    return delta.total_seconds() <= window_minutes * 60

def generate_security_alert(username: str, failures: int) -> str:
    return f'SECURITY ALERT: Multiple failed login attempts detected for {username}. Possible brute force attack.'

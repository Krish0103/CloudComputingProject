import re

WEAK_PASSWORDS = {
    '123456',
    'password',
    'admin',
    'qwerty',
    'letmein',
    'welcome',
    'abc123',
    'iloveyou',
}

PASSWORD_RULES = {
    'length': r'.{8,}',
    'uppercase': r'[A-Z]',
    'lowercase': r'[a-z]',
    'digit': r'\d',
    'special': r'[!@#$%^&*(),.?":{}|<>]'
}

def is_weak_password(password: str) -> bool:
    return password.lower() in WEAK_PASSWORDS

def password_strength(password: str) -> dict:
    results = {}
    for rule, pattern in PASSWORD_RULES.items():
        results[rule] = bool(re.search(pattern, password))
    results['weak_password'] = is_weak_password(password)
    return results

def strength_score(password: str) -> int:
    score = 0
    checks = password_strength(password)
    for key, value in checks.items():
        if key != 'weak_password' and value:
            score += 1
    if checks['weak_password']:
        score = max(score - 2, 0)
    return score

def strength_summary(password: str) -> str:
    score = strength_score(password)
    if score <= 2:
        return 'Very Weak'
    elif score == 3:
        return 'Weak'
    elif score == 4:
        return 'Medium'
    else:
        return 'Strong'

def check_password(password: str) -> dict:
    checks = password_strength(password)
    return {
        'password': password,
        'weak_password': checks['weak_password'],
        'length_ok': checks.get('length', False),
        'uppercase_ok': checks.get('uppercase', False),
        'lowercase_ok': checks.get('lowercase', False),
        'digit_ok': checks.get('digit', False),
        'special_ok': checks.get('special', False),
        'score': strength_score(password),
        'summary': strength_summary(password)
    }

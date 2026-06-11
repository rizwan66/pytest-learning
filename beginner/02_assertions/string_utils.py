def reverse(s):
    return s[::-1]

def is_palindrome(s):
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def word_count(s):
    if not s.strip():
        return 0
    return len(s.split())

def capitalize_words(s):
    return " ".join(word.capitalize() for word in s.split())

def truncate(s, max_length, suffix="..."):
    if len(s) <= max_length:
        return s
    return s[:max_length] + suffix

def extract_emails(text):
    import re
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

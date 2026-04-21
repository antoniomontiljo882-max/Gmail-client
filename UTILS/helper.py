import os
import time
import email
from email.header import decode_header
import base64
import re


DOMAIN_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)


def clear():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def load_domains(file_path):
    """Reads a file and returns a list of non-empty domain strings."""
    domains = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = DOMAIN_PATTERN.search(line)

            if match:
                domains.append(match.group(0).lower())

    return domains


def build_uids(emails):
    """Joins a list of email UID bytes into a single comma-separated byte string."""
    uid_bytes = b",".join(emails)
    return uid_bytes


def timer(start=None):
    """Returns the current time if no argument is given, otherwise returns the elapsed time since start."""
    if start is None:
        return time.perf_counter()

    elapsed = time.perf_counter() - start
    return elapsed


def decode_mime_words(s):
    """Decodes MIME-encoded words in a string into a readable UTF-8 format."""
    if not s:
        return ""

    decoded_parts = decode_header(s)
    decoded_string = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            if encoding in (None, "unknown-8bit"):
                encoding = "utf-8"
            decoded_string += part.decode(encoding, errors="ignore")
        else:
            decoded_string += part

    return decoded_string


def parse_email(raw_bytes):
    """Parses raw email bytes into a structured email message object."""
    return email.message_from_bytes(raw_bytes)


def extract_domain(data):
    """Extracts domains from email 'from' fields and returns a dictionary with their occurrence count."""
    domains = {}

    for item in data:
        sender = item.get("from", "")
        email_address = sender.split("<")[-1].replace(">", "")
        domain = email_address.split("@")[-1]

        if domain:
            if domain not in domains:
                domains[domain] = 1
            else:
                domains[domain] += 1

    return domains


def write_txt(path, text):
    """Appends a domain to a file if valid and not already present."""
    normalized = text.strip().lower()
    match = DOMAIN_PATTERN.fullmatch(normalized)

    if not match:
        return "invalid"

    existing_domains = set(load_domains(path))
    if normalized in existing_domains:
        return "exists"

    with open(path, "a", encoding="utf-8") as file:
        file.write(normalized + "\n")

    return "added"


def decode_imap_utf7(s):
    """Decodes IMAP modified UTF-7 encoded folder names into readable UTF-8."""
    result = ""
    i = 0

    while i < len(s):
        if s[i] == '&':
            j = s.find('-', i)
            if j == -1:
                result += s[i:]
                break

            if j == i + 1:
                result += '&'
            else:
                b64 = s[i+1:j].replace(',', '/')

                padding = '=' * (-len(b64) % 4)
                b64 += padding

                try:
                    decoded = base64.b64decode(b64)
                    result += decoded.decode('utf-16-be')
                except Exception:
                    
                    result += s[i:j+1]

            i = j + 1
        else:
            result += s[i]
            i += 1

    return result

if __name__ == "__main__":

    tests = [
        "INBOX",
        "[Gmail]",
        "Entw&APw-rfe",
        "Gel&APY-scht",
        "Wichtig",
        "Test&-Ordner",
        "Entw&APw-rfe123",
    ]

    print("--- TEST decode_imap_utf7 ---\n")

    for t in tests:

        decoded = decode_imap_utf7(t)
        print(f"RAW:     {t}")
        print(f"DECODED: {decoded}")
        print("-"*30)

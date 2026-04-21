# Gmail Automation Tool

CLI tool for managing a Gmail inbox via IMAP.

The project focuses on handling large inboxes with UID-based IMAP operations,
domain statistics, and bulk moves to spam.

## Features

- Connects to Gmail over IMAP
- Fetches email headers by UID
- Extracts sender domains
- Shows domain frequency statistics
- Moves emails from configured domains to spam in bulk
- Keeps local credentials out of Git

## Requirements

- Python 3.10+
- Gmail account
- IMAP enabled in Gmail
- Google App Password

## Setup

```bash
git clone https://github.com/antoniomontiljo882-max/Gmail-client.git
cd Gmail-client
pip install -r requirements.txt
```

Create a local `.env` file:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_google_app_password
```

You can copy the structure from `.env.example`.

## Run

```bash
python main.py
```

## Project Structure

- `main.py` - CLI entry point and menu flow
- `services/` - IMAP operations
- `UI/` - terminal display and email transformation
- `UTILS/` - helper functions and terminal colors
- `txt_files/domains_adresses.txt` - domains used for bulk actions

## Performance Notes

- Uses IMAP UIDs instead of sequence numbers for stable operations
- Fetches email data in chunks to avoid oversized IMAP responses
- Fetches only needed header fields where possible
- Uses mailbox metadata for inbox counts instead of searching every UID
- Expunges once after bulk moves instead of after every sender batch

## Notes

This tool is intended for local use with real Gmail data. Do not commit `.env`
or app passwords.

## Possible Next Steps

- Add rule-based automation
- Add structured logging
- Add pagination for very large folder views
- Add tests around domain extraction and IMAP response parsing

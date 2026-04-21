import time

from UTILS.colors import (
    dim, bold, bright_white, bright_magenta, bright_yellow, red,
    cyan, yellow, bright_red, grey, white, underline,
    blink, reverse, bg_yellow, bg_blue, bg_white, bg_cyan, bg_green,
    bg_magenta, bg_red, bright_blue, blue, magenta, green
)

from UTILS.helper import decode_imap_utf7
from services.imap_client import fetch_all_emails, get_email_count, get_email_uids
from UI.email_transformer import build_email_dataset


def show_domain_statistics(domains):
    """Displays sorted domain statistics with counts and visual bars."""

    print(bold(bright_magenta("\nDOMAIN STATISTICS\n")))

    for i, item in enumerate(domains, 1):
        

        domain = item[0]
        count = item[1]

        index = f"{str(i) + '.':>2}"
        dom = f"{domain:<38}"
        cnt = f"{str(count):>5}"
        bars = "█" * max(1, count // 5)

        print("\n", dim(green(index)) + " " + white(dom) + " " + bold(yellow(cnt)) + "  " + cyan(bars))

    print()


def clean_folder_name(folder):
    """Returns a cleaner version of a folder name for display only."""

    if "/" in folder:
        return folder.split("/")[-1]

    if folder == "[Gmail]":
        return "Gmail"

    return folder


def show_folder_content(email_objekt, folder_name):
    """Opens a folder, fetches its emails, and renders the email overview."""

    display_name = clean_folder_name(folder_name)
    display_name = decode_imap_utf7(display_name)

    print(bold(green(f"\nOpened folder: {bold(white(display_name))}\n")))
    time.sleep(1)

    try:
        data = get_email_uids(email_objekt, "All", f'"{folder_name}"')
    except Exception as e:
        print(red(f"Error opening folder: {display_name}"))
        print(grey(str(e)))
        return

    if not data:
        print(red(f"\n{display_name}"), "contains no emails.")
        return

    raw = fetch_all_emails(
        email_objekt,
        data,
        "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE MESSAGE-ID)])"
    )
    dataset = build_email_dataset(raw)

    render_email_list(dataset, display_name)


def show_folders(email_objekt):
    """Retrieves and displays all available email folders."""

    status, folders = email_objekt.list()

    if status != "OK":
        print("Could not fetch folders")
        return []

    names = []

    print("\nAvailable folders:\n")

    index = 1

    for folder in folders:
        decoded = folder.decode()  

        raw_name = decoded.split(' "/" ')[-1].strip('"')
         
        display_name = clean_folder_name(raw_name)
        display_name = decode_imap_utf7(display_name)
       
    

        if display_name == "Gmail":
            continue

        names.append(raw_name)  

        print(f"{green(str(index))} {grey('›')} {white(display_name)}")

        index += 1

    return names


def render_email_list(dataset, folder):
    """Renders a formatted overview of all emails in the selected folder."""
    width = 72

    print()
    print(bold(bright_magenta(" MAIL OVERVIEW ".center(width, "="))))
    print()

    delay = 0

    if len(dataset) < 150:
        delay = 0.1

    for i, mail in enumerate(dataset, 1):
        subject = bright_white((mail.get("subject") or "").strip()) if (mail.get("subject") or "").strip() else red("No subject")
        sender = (mail.get("from") or "Unknown sender").strip()
        to = (mail.get("to") or "Unknown sender").strip()
        date = (mail.get("date") or "Unknown date").strip()
        uid = (mail.get("uid") or "N/A")

        print(dim("┌" + "─" * (width - 2) + "┐"))
        print(f"{dim(green(f'[{i}]'))} {bold(subject[:width - 10])}")
        print(dim("│"))
        print(f"{bold(dim('From:'.ljust(8)))}{magenta(sender[:width - 12])}")
        print(f"{dim('To:'.ljust(8))}{green(to[:width - 12])}")
        print(f"{dim('Date:'.ljust(8))}{bright_yellow(date[:width - 12])}")
        print(dim("└" + "─" * (width - 2) + "┘"))
        print()

        if delay:
            time.sleep(delay)

    print(green(f"Total emails in {bold(white(folder))}: {white(len(dataset))}"))
    print()


def show_existing_domains(path):
    """Reads and prints all stored domains from a file."""

    with open(path, "r", encoding="utf-8") as f:
        domains = f.read()

        print(dim("─"*40))
        print(white(domains))
        print(dim("─"*40))
        

def render_main_menu(email_objekt, email):
    """Displays the main menu and returns the user's selected command."""

    email_count = get_email_count(email_objekt)

    title = "GMAILGUARD"
    account_line = f"{email}"
    emails_line = f"{email_count}"

    content_width = max(len(title), len(account_line), len(emails_line)) + 20
    header = "═" * content_width

    print()
    print(bright_magenta(header))
    print(bold(bright_white(title.center(content_width))))
    print(bright_magenta(header))
    print()

    print(bold(grey("STATUS")))
    print(dim("─" * content_width))

    print(
        bright_magenta(" Account ")
        + bright_white("│ ")
        + underline(bright_white(account_line))
    )
    print()
    print(
        green(" Emails ")
        + bright_white(" │ ")
        + white(emails_line)
    )

    print()
    print(dim("─" * content_width))
    print()

    print(bold(grey("COMMANDS")))
    print(dim("─" * content_width))

    print(green(" 1") + grey(" → ") + white("Show folder content"))
    print(green(" 2") + grey(" → ") + white("Move domain to spam"))
    print(green(" 3") + grey(" → ") + white("Show most common domains"))
    print(green(" 4") + grey(" → ") + white("Add domains"))
    print(bright_red(" 5") + grey(" → ") + white("Exit"))


    print()
    print(dim("─" * content_width))

    choice = input(magenta("\n command › "))
    print()

    return choice


if __name__ == "__main__":
    pass

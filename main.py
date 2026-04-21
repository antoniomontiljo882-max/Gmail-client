from UTILS.colors import (
    blue, red, yellow, bold, bright_yellow,
    bright_blue, magenta, cyan, dim,
    bright_magenta, bright_red, bright_white,
    green, grey, white
)

from UTILS.helper import (
    load_domains,
    extract_domain, write_txt, clear, timer
)

from services.imap_client import (
    login_imap, get_email_uids, fetch_all_emails,
    fetch_one_email, move_email, move_all_emails
)

from UI.email_transformer import build_email_dataset

from UI.display import (
    show_folder_content,
    show_domain_statistics,
    show_folders,
    render_email_list,
    render_main_menu,
    show_existing_domains
)

import time

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")

if not EMAIL or not APP_PASSWORD:
    print(red("\n[ERROR] Missing credentials."))
    print(red("Create a .env file based on .env.example\n"))
    exit()
    




# ============================================================
# PROGRAM START
# ============================================================

def main():

    clear()
    email_objekt = login_imap(EMAIL, APP_PASSWORD)
    clear()

    while True:

        clear()
        choice = render_main_menu(email_objekt, EMAIL)

        # --------------------------------------------------------
        # SHOW FOLDER CONTENT
        # --------------------------------------------------------
        if choice == "1":

            folders = show_folders(email_objekt)

            print()
            raw_option = input("Select folder → ").strip()
            print()

            if not raw_option.isdigit():
                print(red("Invalid input. Please type a number."))
                input(bold(grey("RETURN (Enter)\n")))
                continue

            option = int(raw_option)
            if option < 1 or option > len(folders):
                print(red("Invalid folder number."))
                input(bold(grey("RETURN (Enter)\n")))
                continue

            selected = folders[option - 1]
            show_folder_content(email_objekt, selected)

            print()
            input(bold(grey("RETURN (Enter)\n")))

        # --------------------------------------------------------
        # MOVE DOMAIN TO SPAM
        # --------------------------------------------------------
        elif choice == "2":

            print(dim("─────────────────────────────"))

            senders = load_domains("txt_files/domains_adresses.txt")

            print(bright_magenta("Moving emails to spam...\n"))

            counter = move_all_emails(email_objekt, senders, "[Gmail]/Spam")

            print(dim("─" * 30))
            print()
            print(green(f"✔️  Done - {counter} emails moved"))
            print()

            input(bold(grey("RETURN (Enter)\n")))
        # --------------------------------------------------------
        # SHOW DOMAIN STATISTICS
        # --------------------------------------------------------
        elif choice == "3":

            print(bright_yellow("Analyzing domains...\n"))

            email_uids = get_email_uids(email_objekt)

            fetch_mails = fetch_all_emails(
                email_objekt,
                email_uids,
                "(BODY.PEEK[HEADER.FIELDS (FROM)])"
            )
            data_set = build_email_dataset(fetch_mails)

            domains = extract_domain(data_set)

            sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)

            show_domain_statistics(sorted_domains)

            print()

            while True:
                domain = input(yellow("\nType new domain-name or (q) to return:\n")).strip()

                if domain.lower() == "q":
                    break

                if not domain:
                    print(red("Empty input. Try again."))
                    continue

                status = write_txt("txt_files/domains_adresses.txt", domain)

                print()
                if status == "added":
                    print(green(f"Added {white(domain.lower())}"))
                elif status == "exists":
                    print(yellow(f"Already exists: {white(domain.lower())}"))
                else:
                    print(red("Invalid domain format."))

            print()
            input(bold(grey("RETURN (Enter)\n")))



        elif choice == "4":

            print()
            print(yellow("Active domains..."))
            time.sleep(1)

            show_existing_domains("txt_files/domains_adresses.txt")

            while True:
                domain = input(yellow("\nType new domain-name or (q) to return:\n")).strip()

                if domain.lower() == "q":
                    break

                if not domain:
                    print(red("Empty input. Try again."))
                    continue

                status = write_txt("txt_files/domains_adresses.txt", domain)

                print()
                if status == "added":
                    print(green(f"Added {white(domain.lower())}"))
                elif status == "exists":
                    print(yellow(f"Already exists: {white(domain.lower())}"))
                else:
                    print(red("Invalid domain format."))

            print()
            input(bold(grey("RETURN (Enter)\n")))

            



        elif choice == "5":

            print(bright_red("\nさようなら...\n"))
            email_objekt.logout()
            break

        # --------------------------------------------------------
        # INVALID INPUT
        # --------------------------------------------------------
        else:

            print(bright_red("Invalid option.\n"))


if __name__ == "__main__":
    main()

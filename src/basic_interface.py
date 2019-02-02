import sys

from Cli import Cli

cli = Cli()
skip = 0


def user_choice():
    """Handles interface choice interaction."""
    global skip
    choice = cli.prompt().lower()
    if choice == "":
        print("Please, input one of the options or a new tweet.")
    if choice == "0":
        sys.exit(0)
    elif choice == "m":
        skip += 5
        cli.print_alternative_views(skip)
    elif choice == "n":
        skip = 0
        cli.init_prompt()
    elif choice in range(0, skip + 5):
        cli.set_central(cli.get_tweet(choice))
        skip = 0
        cli.print_alternative_views()
    else:
        skip = 0
        cli.set_central(choice)
        cli.print_alternative_views()
    user_choice()


if __name__ == "__main__":
    cli.init_prompt()
    user_choice()

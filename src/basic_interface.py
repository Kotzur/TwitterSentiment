import sys

from src.Cli import Cli

cli = Cli()
skip = 0


def user_choice():
    global skip
    choice = cli.prompt().lower()
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
    # TODO: Fix recognizing
    else:
        skip = 0
        cli.set_central(choice)
        cli.print_alternative_views()
    user_choice()


if __name__ == "__main__":
    cli.init_prompt()
    user_choice()

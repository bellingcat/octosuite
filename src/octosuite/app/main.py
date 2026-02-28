from .cli import run_cli
from .cli.main import arg_parser
from .tui import run_tui


def start_app():
    parser = arg_parser()
    args = parser.parse_args()

    if args.tui:
        run_tui()
    if args.command:
        run_cli(args=args)
    else:
        parser.print_usage()

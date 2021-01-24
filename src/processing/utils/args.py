import sys
import optparse


def create_parser():
    """
    Adds various command-line arguments supported by the processing script.
    """
    parser = optparse.OptionParser()

    parser.add_option(
        "-t",
        "--threads",
        action="store",
        dest="threads",
        help="The number of worker threads to use while processing results.",
        default=4,
        type=int
    )
    parser.add_option(
        "-f",
        "--firstrun",
        action="store_true",
        dest="firstrun",
        help="Executes with 'first run' parameters (gets results from last 24h)",
        default=False
    )
    parser.add_option(
        "-m",
        "--minute",
        action="store",
        dest="hourly_min",
        help="The minute when the hourly processor executes",
        default=15,
        type=int
    )
    parser.add_option(
        "-d",
        "--drop-db",
        action="store_true",
        dest="drop_db",
        help="Drops VisIBoT database before initializing processing script. Before dropping, you will be asked to confirm this action.",
        default=False
    )

    return parser


def check_options():
    """
    Validates the command-line arguments provided by the user.

    Raises:
        SystemExit: If option is provided invalid value, print error and exit
    """
    parser = create_parser()
    options, args = parser.parse_args()

    threads_ok = options.threads >= 1
    hour_min_ok = 0 <= options.hourly_min <= 59

    if (threads_ok and hour_min_ok):
        return options

    err_msg = "error: invalid parameter(s)"

    if not threads_ok:
        err_msg = "\n".join([err_msg, " -f, --firstrun: Number of threads must be at least 1."])
    if not hour_min_ok:
        err_msg = "\n".join([err_msg, " -m, --minute: Minute value must be between 0-59."])

    print(err_msg, file=sys.stderr)

    raise SystemExit()

import os
import sys
import logging
import argparse
import subprocess

try:
    from PyQt5.uic import loadUiType
    pyuic_version = "pyuic5"
except ImportError:
    from PyQt4.uic import loadUiType
    pyuic_version = "pyuic4"

logger = logging.getLogger(__name__)


class IndentPrinter(object):
    def __init__(self, outfile=sys.stdout, char=' ', width=4):
        self.char = char
        self.width = width
        # When you instanciate the context manager, you set level += 1
        self.level = -1
        self.outfile = outfile

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, value, type, traceback):
        self.level -= 1

    def write(self, txt):
        self.outfile.write(
            '%s%s' % (self.char * (self.width * self.level), txt))


def pyqt3wrapper_generator(uifile, outfile, indent_width=4, from_imports=False,
                           resource_suffix="_rc"):
    # return a tuple of the generated form class and the Qt base class
    parser = loadUiType(uifile, from_imports, resource_suffix)
    class_name_ui = parser[0].__name__
    class_name = class_name_ui.replace('Ui_', '')
    inherit_widgetname = parser[1].__name__
    with IndentPrinter(outfile, width=indent_width) as f:
        f.write('class {0}(QtGui.{1}, {2}):\n'.format(
            class_name, inherit_widgetname, class_name_ui))
        with f:
            x = "def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):\n"
            f.write(x)
            with f:
                f.write('QtGui.{0}.__init__(self, parent, f)\n\n'.format(
                    inherit_widgetname))
                f.write('self.setupUi(self)\n')


def main():
    parser = argparse.ArgumentParser(
        description="Generates PyQt3 style wrapper for pyuic.")
    parser.add_argument("inputfile", help="input ui filename", nargs="?")
    parser.add_argument(
        "-o", "--outputfile",
        default="-",
        help="output generate file")
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="overwrite your outputfile")
    parser.add_argument(
        "-i", "--indent",
        action="store", type=int,
        default=4, metavar="N",
        help="set indent width to N spaces, tab if N is 0 [default: 4]")
    parser.add_argument(
        "--pyuic",
        default=os.environ.get("PYUIC_PATH", pyuic_version),
        help="path to pyuic binary")

    pyuic_group = parser.add_argument_group(
        "pyuic", "options passed to pyuic (see pyuic --help)")
    pyuic_group.add_argument(
        "-x", "--execute",
        action="store_true")
    pyuic_group.add_argument(
        "-d", "--debug",
        action="store_true")
    generation_option = parser.add_argument_group(
        "Code generation option:")
    generation_option.add_argument(
        "--from_imports",
        action="store_true",
        default=False,
        help="generate imports relative to '.'")
    generation_option.add_argument(
        "--version",
        action="store_true",
        help="print pyuic --version")
    generation_option.add_argument(
        "--resource_suffix", action="store",
        type=str, default="_rc", metavar="SUFFIX",
        help="append SUFFIX to the basename of resource files [default: _rc]")
    args, _ = parser.parse_known_args()

    loghandler = logging.StreamHandler(sys.stderr)
    loghandler.setLevel(args.debug and logging.DEBUG or logging.WARNING)
    loghandler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.setLevel(args.debug and logging.DEBUG or logging.WARNING)
    logger.addHandler(loghandler)

    pyuic_command = [args.pyuic, ]

    if args.version:
        pyuic_command.append("--version")
        logger.debug("execute command: %s", pyuic_command)
        return subprocess.call(pyuic_command, close_fds=True, shell=False)
    else:
        if not args.inputfile:
            parser.print_help()
            return 1

    pyuic_command.extend([args.inputfile, "-o", args.outputfile])
    if args.execute:
        pyuic_command.append("-x")
    if args.debug:
        pyuic_command.append("-d")
    if args.indent:
        pyuic_command.extend(["-i", str(args.indent)])
    if args.from_imports:
        pyuic_command.append("--from-imports")
    if args.resource_suffix:
        pyuic_command.extend(["--resource-suffix", str(args.resource_suffix)])

    sys.path.insert(0, os.getcwd())

    logger.info("pyuic command: %s", pyuic_command)

    try:
        inputfile = open(args.inputfile)
    except (IOError, OSError):
        logger.critical("Unable to open input file: %s", args.inputfile)
        return 1

    if args.outputfile == "-":
        outputfile = sys.stdout
    else:
        if os.path.exists(args.outputfile) and not args.force:
            logger.critical("Your file exists. Use -f option for overwrite it")
            return 2
        outputfile = open(args.outputfile, "w")

    try:
        ret = subprocess.call(
            pyuic_command, close_fds=True, shell=False)
        if ret != 0:
            logger.fatal("pyuic generator FAILED")
            return ret
        logger.info("pyuic generator FINISHED")
        outputfile.seek(0, 2)
        pyqt3wrapper_generator(
            inputfile, outputfile, args.indent,
            args.from_imports, args.resource_suffix)
    finally:
        outputfile.close()
        inputfile.close()
        logger.info('Success')
    return 0


if __name__ == "__main__":
    sys.exit(main())

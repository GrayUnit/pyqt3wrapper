#!/usr/bin/env python

import io
import os
import unittest
import tempfile
import subprocess
from pyqt3wrapper.pyuic_pyqt3wrapper import (IndentPrinter,
                                             pyqt3wrapper_generator)


class IndentPrinterTestCase(unittest.TestCase):
    def test_indent(self):
        with open(os.path.join("tests", "output", "indent_test1")) as f:
            expected_output = f.readlines()
            print("expected_output: %s" % expected_output)

        with io.BytesIO() as fileinput:
            with IndentPrinter(fileinput) as f:
                f.write("class Foo(object):\n")
                with f:
                    f.write("def bar(self):\n")
                    with f:
                        f.write("pass\n")
                f.write("\n")
                with f:
                    f.write("def haha(self):\n")
                    with f:
                        f.write("self.setupUi(self)\n")
            fileinput.seek(0)
            assert expected_output == fileinput.readlines()


class PyQt3WrapperTestCase(unittest.TestCase):
    _subprocess_args = {"shell": False, "close_fds": True}
    _exec_name = "pyuic_pyqt3wrapper.py"

    def test_wrapper(self):
        with tempfile.NamedTemporaryFile(delete=False) as outputfile:
            fileinputname = open(os.path.join("tests", "ui", "test1.ui"))
            expected_output = open(
                os.path.join("tests", "output", "test_wrapper")).readlines()
            pyqt3wrapper_generator(fileinputname, outputfile)
            outputfile.seek(0)
            outresult = outputfile.readlines()
            assert(outresult == expected_output)

    def _test_call_pyqt3wrapper(self, expected_output_filename, cmd):
        with open(expected_output_filename, "r") as f:
            output_expected = f.readlines()
        with tempfile.NamedTemporaryFile(delete=False) as outputfile:
            cmd += [outputfile.name, ]
            assert subprocess.call(cmd, **self._subprocess_args) == 0
            outputfile = self._strip(outputfile)
            with outputfile as f:
                outresult = f.readlines()
            assert(outresult == output_expected)

    def test_generate(self):
        self._test_call_pyqt3wrapper(
            os.path.join("tests/output/test_pyuicwrapper"),
            [self._exec_name, "-f",
                os.path.join("tests", "ui", "test1.ui"), "-o"])

    def test_pyuicargs(self):
        self._test_call_pyqt3wrapper(
            os.path.join("tests/output/test_pyuicexecute"),
            [self._exec_name, "-f", "-x", "-d",
                os.path.join("tests", "ui", "test1.ui"), "-o"])

    def test_fileopen(self):
        subprocess.call([
            self._exec_name,
            os.path.join("tests", "ui", "test1.ui"),
            "-o",
            os.path.join("tests", "output", "test_pyuicwrapper")],
            **self._subprocess_args)
        assert SystemExit(2)

    def _strip(self, outputfile):
        tmpout = tempfile.NamedTemporaryFile(delete=False)
        with outputfile as fin:
            with tmpout as fout:
                fin.seek(0)
                for line in fin.readlines():
                    if line.startswith("# Created"):
                        fout.write("# Created: stripped\n")
                    elif line.startswith("#      by:"):
                        fout.write("#      by: PyQt\n")
                    else:
                        fout.write(line)
        os.unlink(outputfile.name)
        return open(fout.name, "r")

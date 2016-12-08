#!/usr/bin/env python
# -*- coding: utf8 -*-
"""A script to ensure that our docs are not being utterly neglected."""
import argparse
import os
import sys

IGNORES = {
    'pydir': ['tests'],
    'pyfile': ['__init__.py'],
    'docfile': ['index.rst'],
}


class AddDocIgnores(argparse.Action):
    """Add entries to docfile ignores list."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Add entries to docfile ignores list."""
        global IGNORES
        ignores = values.split(',')
        IGNORES['docfile'] += ignores
        setattr(namespace, 'doc_ignores', ignores)


class DocParityCheck(object):
    """Ensure proper python module and documentation parity."""

    def __init__(self):
        self._args = None

    @property
    def args(self):
        """Parsed command-line arguments."""
        if self._args is None:
            parser = self._build_parser()
            self._args = parser.parse_args()
        return self._args

    def build_pypackage_basename(self, pytree, base):
        """Build the string representing the parsed package basename.

        :param str pytree: The pytree absolute path.
        :param str pytree: The absolute path of the pytree sub-package of which determine the
            parsed name.
        :rtype: str
        """
        dirname = os.path.dirname(pytree)
        parsed_package_name = base.replace(dirname, '').strip('/')
        return parsed_package_name

    def _build_parser(self):
        """Build the needed command-line parser."""
        parser = argparse.ArgumentParser()

        parser.add_argument('--pytree',
                            required=True,
                            type=self._valid_directory,
                            help='This is the path, absolute or relative, of the Python package '
                                 'that is to be parsed.')

        parser.add_argument('--doctree',
                            required=True,
                            type=self._valid_directory,
                            help='This is the path, absolute or relative, of the documentation '
                                 'package that is to be parsed.')

        parser.add_argument('--no-fail',
                            action='store_true',
                            help='Using this option will cause this program to return an exit '
                                 'code of 0 even when the given trees do not match.')

        parser.add_argument('--doc-ignores',
                            action=AddDocIgnores,
                            help='A comma separated list of additional doc files to ignore')

        return parser

    def build_rst_name_from_pypath(self, parsed_pypath):
        """Build the expected rst file name based on the parsed Python module path.

        :param str parsed_pypath: The parsed Python module path from which to build the expected
            rst file name.
        :rtype: str
        """
        expected_rst_name = parsed_pypath.replace('/', '.').replace('.py', '.rst')
        return expected_rst_name

    def build_pyfile_path_from_docname(self, docfile):
        """Build the expected Python file name based on the given documentation file name.

        :param str docfile: The documentation file name from which to build the Python file name.
        :rtype: str
        """
        name, ext = os.path.splitext(docfile)
        expected_py_name = name.replace('.', '/') + '.py'
        return expected_py_name

    def calculate_tree_differences(self, pytree, doctree):
        """Calculate the differences between the given trees.

        :param dict pytree: The dictionary of the parsed Python tree.
        :param dict doctree: The dictionary of the parsed documentation tree.
        :rtype: tuple
        :returns: A two-tuple of sets, where the first is the missing Python files, and the second
            is the missing documentation files.
        """
        pykeys = set(pytree.keys())
        dockeys = set(doctree.keys())

        # Calculate the missing documentation files, if any.
        missing_doc_keys = pykeys - dockeys
        missing_docs = {pytree[pyfile] for pyfile in missing_doc_keys}

        # Calculate the missing Python files, if any.
        missing_py_keys = dockeys - pykeys
        missing_pys = {docfile for docfile in missing_py_keys}

        return missing_pys, missing_docs

    def compare_trees(self, parsed_pytree, parsed_doctree):
        """Compare the given parsed trees.

        :param dict parsed_pytree: A dictionary representing the parsed Python tree where each
            key is a parsed Python file and its key is its expected rst file name.
        """
        if parsed_pytree == parsed_doctree:
            return 0

        missing_pys, missing_docs = self.calculate_tree_differences(pytree=parsed_pytree,
                                                                    doctree=parsed_doctree)
        self.pprint_tree_differences(missing_pys=missing_pys, missing_docs=missing_docs)
        return 0 if self.args.no_fail else 1

    def _ignore_docfile(self, filename):
        """Test if a documentation filename should be ignored.

        :param str filename: The documentation file name to test.
        :rtype: bool
        """
        if filename in IGNORES['docfile'] or not filename.endswith('.rst'):
            return True
        return False

    def _ignore_pydir(self, basename):
        """Test if a Python directory should be ignored.

        :param str filename: The directory name to test.
        :rtype: bool
        """
        if basename in IGNORES['pydir']:
            return True
        return False

    def _ignore_pyfile(self, filename):
        """Test if a Python filename should be ignored.

        :param str filename: The Python file name to test.
        :rtype: bool
        """
        if filename in IGNORES['pyfile'] or not filename.endswith('.py'):
            return True
        return False

    def parse_doc_tree(self, doctree, pypackages):
        """Parse the given documentation tree.

        :param str doctree: The absolute path to the documentation tree which is to be parsed.
        :param set pypackages: A set of all Python packages found in the pytree.
        :rtype: dict
        :returns: A dict where each key is the path of an expected Python module and its value is
            the parsed rst module name (relative to the documentation tree).
        """
        parsed_doctree = {}
        for filename in os.listdir(doctree):
            if self._ignore_docfile(filename):
                continue

            expected_pyfile = self.build_pyfile_path_from_docname(filename)
            parsed_doctree[expected_pyfile] = filename

        pypackages = {name + '.py' for name in pypackages}
        return {elem: parsed_doctree[elem] for elem in parsed_doctree if elem not in pypackages}

    def parse_py_tree(self, pytree):
        """Parse the given Python package tree.

        :param str pytree: The absolute path to the Python tree which is to be parsed.
        :rtype: dict
        :returns: A two-tuple. The first element is a dict where each key is the path of a parsed
            Python module (relative to the Python tree) and its value is the expected rst module
            name. The second element is a set where each element is a Python package or
            sub-package.
        :rtype: tuple
        """
        parsed_pytree = {}
        pypackages = set()
        for base, dirs, files in os.walk(pytree):
            if self._ignore_pydir(os.path.basename(base)):
                continue

            # TODO(Anthony): If this is being run against a Python 3 package, this needs to be
            # adapted to account for namespace packages.
            elif '__init__.py' not in files:
                continue

            package_basename = self.build_pypackage_basename(pytree=pytree, base=base)
            pypackages.add(package_basename)

            for filename in files:
                if self._ignore_pyfile(filename):
                    continue

                parsed_path = os.path.join(package_basename, filename)
                parsed_pytree[parsed_path] = self.build_rst_name_from_pypath(parsed_path)

        return parsed_pytree, pypackages

    def pprint_tree_differences(self, missing_pys, missing_docs):
        """Pprint the missing files of each given set.

        :param set missing_pys: The set of missing Python files.
        :param set missing_docs: The set of missing documentation files.
        :rtype: None
        """
        if missing_pys:
            print('The following Python files appear to be missing:')
            for pyfile in missing_pys:
                print(pyfile)
            print('\n')

        if missing_docs:
            print('The following documentation files appear to be missing:')
            for docfiile in missing_docs:
                print(docfiile)
            print('\n')

    def _valid_directory(self, path):
        """Ensure that the given path is valid.

        :param str path: A valid directory path.
        :raises: :py:class:`argparse.ArgumentTypeError`
        :returns: An absolute directory path.
        """
        abspath = os.path.abspath(path)
        if not os.path.isdir(abspath):
            raise argparse.ArgumentTypeError('Not a valid directory: {}'.format(abspath))
        return abspath

    def main(self):
        """Parse package trees and report on any discrepancies."""
        args = self.args
        parsed_pytree, pypackages = self.parse_py_tree(pytree=args.pytree)
        parsed_doctree = self.parse_doc_tree(doctree=args.doctree, pypackages=pypackages)
        return self.compare_trees(parsed_pytree=parsed_pytree, parsed_doctree=parsed_doctree)


if __name__ == '__main__':
    sys.exit(DocParityCheck().main())

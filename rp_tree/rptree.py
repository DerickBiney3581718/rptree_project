"""main module for rptree functionality
    """

import os
import pathlib


PIPE = "|"
ELBOW = '|___'
TEE = "|---"

PIPE_PREFIX = "|   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root_dir, dir_only=False, output_file=None):
        self._generator = _TreeGenerator(root_dir, dir_only)
        self.output_file = output_file

    def generate(self):
        tree = self._generator.build_tree()
        if not self.output_file:
            for entry in tree:
                print(entry)
        else:
            with open(self.output_file, "w") as f:
                f.write('\n'.join(tree))


class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._tree = []
        self._dir_only = dir_only

    def build_tree(self):
        self._build_head()
        self._build_body(self._root_dir)
        return self._tree

    def _build_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _build_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())

        entries_count = len(entries)

        for ind, entry in enumerate(entries):
            connector = ELBOW if ind == entries_count - 1 else TEE

            if entry.is_dir():
                self._add_directory(
                    entry, ind, entries_count, prefix, connector
                )
            else:
                if not self._dir_only:
                    self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        # ~- self.__build_head
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")

        if index != entries_count:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX

        self._build_body(directory=directory, prefix=prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file}")

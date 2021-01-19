from pathlib import Path


class PathTree(object):
    # Set up spacer character defs
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '│   '
    display_parent_prefix_last = '    '
    max_children = 1000

    def __init__(self, path, parent_path, is_last, max_depth):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        self.max_depth = max_depth
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def display_name(self):
        out_str = self.path.name
        if self.path.is_dir():
            out_str += '/'  # add directory /
        return out_str + ("   -- Max depth ({}) for scan-input logfile reached. ".format(self.max_depth) if self.depth == self.max_depth else "")

    @classmethod
    def make_tree(cls, root, max_depth=6, parent=None, is_last=False):
        root = Path(str(root))
        displayable_root = cls(root, parent, is_last, max_depth)
        yield displayable_root
        if displayable_root.depth < max_depth:
            children = sorted(list(path for path in root.iterdir()), key=lambda s: str(s).lower())
            count = 1

            for path in children[0:min(PathTree.max_children, len(children))]:
                is_last = count == len(children) or displayable_root.depth+1 == max_depth
                if path.is_dir():
                    yield from cls.make_tree(path,
                                             parent=displayable_root,
                                             is_last=is_last,
                                             max_depth=max_depth)
                else:
                    yield cls(path, displayable_root, is_last, max_depth)
                count += 1

    def displayable(self):
        if self.parent is None:
            return self.display_name

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix, self.display_name)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if not parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent
        return ''.join(reversed(parts))

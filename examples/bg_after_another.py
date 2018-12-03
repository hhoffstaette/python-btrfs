#!/usr/bin/python3

import btrfs
import sys

if len(sys.argv) < 2:
    print("Usage: {} <mountpoint>".format(sys.argv[0]))
    sys.exit(1)


tree = btrfs.ctree.EXTENT_TREE_OBJECTID
min_key = btrfs.ctree.Key(0, 0, 0)
bufsize = btrfs.utils.SZ_4K


def first_block_group_after(fs, key):
    for header, data in btrfs.ioctl.search_v2(fs.fd, tree, min_key, buf_size=bufsize):
        if header.type == btrfs.ctree.BLOCK_GROUP_ITEM_KEY:
            return header


fs = btrfs.FileSystem(sys.argv[1])
while True:
    header = first_block_group_after(fs, min_key)
    if header is None:
        break
    min_key = btrfs.ctree.Key(header.objectid + header.offset,
                              btrfs.ctree.BLOCK_GROUP_ITEM_KEY, 0)
    print('.', end='', flush=True)

print()

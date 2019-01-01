# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The program version."""

MAJOR = 1
MINOR = 0
PATCH = 6

VERSION = '{0}.{1}.{2}'.format(MAJOR, MINOR, PATCH)


def main():
    """Print the version."""

    print('BASIC Lang version {0}'.format(VERSION))


if __name__ == '__main__':
    main()

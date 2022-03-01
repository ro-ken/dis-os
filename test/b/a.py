import os
import sys
from .c import d
def main():
    print("sys.path[0] = ", sys.path[0])
    print("sys.path = ", sys.path)
    print("sys.argv[0] = ", sys.argv[0])
    print("__file__ = ", __file__)
    print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
    print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
    print("os.path.dirname(os.path.realpath(__file__)) = ",
          os.path.dirname(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__)) = ",
          os.path.split(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__))[0] = ",
          os.path.split(os.path.realpath(__file__))[0])
    print("os.getcwd() = ", os.getcwd())
    print("---------------------------------------------------------")
    d.main()
if __name__ == '__main__':
    main()
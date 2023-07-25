import sys
if __name__ == '__main__':
    if sys.prefix != sys.base_prefix:
        venv_name = sys.prefix.split("/")[-1]
        print(venv_name)

from os import getcwd
from race.race import Racing


def main():
    racing_obj = Racing()

    racing_obj.parser_logfile('{}/data/log_example'.format(getcwd()))

    print(racing_obj)


if __name__ == "__main__":
    main()
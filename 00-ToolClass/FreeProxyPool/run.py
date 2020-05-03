import sys
import io

from schedule.scheduler import Schedule

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Schedule()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()

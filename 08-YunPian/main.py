import time
from yunpian import YunPian


def main():
    print('开始测试...')
    print('=' * 100)
    num = 1
    success = 0
    yp = YunPian()
    while num <= 50:
        x = yp.run()

        print(x)
        if x['success']:
            success += 1
        time.sleep(2)
        num += 1
    print('最后测试结果 >> %.2f%%' % (success/num * 100))


if __name__ == '__main__':
    main()

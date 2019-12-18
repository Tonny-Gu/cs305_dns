from threading import Thread
import time


class TimeoutException(Exception):
    pass


def time_limited(timeout):
    def decorator(function):
        def __new_fun(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)
                    self.alive = True

                def run(self):
                    function(*args, **kwargs)

            t = TimeLimited()
            t.start()
            t.join(timeout)

            t.alive = False
            if t.is_alive():
                raise TimeoutException('timeout for %s' % (repr(function)))

        return __new_fun

    return decorator


@time_limited(2)  # 设置运行超时时间2S
def fn_1(secs):
    time.sleep(secs)
    return 'Finished without timeout'


def do_something_after_timeout():
    print('Time out!')


if __name__ == "__main__":
    try:
        print(fn_1(3))  # 设置函数执行3S
    except TimeoutException as e:
        print(str(e))
        do_something_after_timeout()

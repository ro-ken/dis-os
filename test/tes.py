import time


class LazyPerson(object):
    def __init__(self, name):
        self.name = name
        self.watch_tv_func = None
        self.have_dinner_func = None

    def get_up(self):
        print("%s get up at:%s" % (self.name, time.time()))

    def go_to_sleep(self):
        print("%s go to sleep at:%s" % (self.name, time.time()))

    def register_tv_hook(self, watch_tv_func):
        self.watch_tv_func = watch_tv_func

    def register_dinner_hook(self, have_dinner_func):
        self.have_dinner_func = have_dinner_func

    def enjoy_a_lazy_day(self):

        # get up
        self.get_up()
        time.sleep(3)
        # watch tv
        # check the watch_tv_func(hooked or unhooked)
        # hooked
        if self.watch_tv_func is not None:
            self.watch_tv_func(self.name)
        # unhooked
        else:
            print("no tv to watch")
        time.sleep(3)
        # have dinner
        # check the have_dinner_func(hooked or unhooked)
        # hooked
        if self.have_dinner_func is not None:
            self.have_dinner_func(self.name)
        # unhooked
        else:
            print("nothing to eat at dinner")
        time.sleep(3)
        self.go_to_sleep()


def watch_daydayup(name):
    print("%s : The program ---day day up--- is funny!!!" % name)


def watch_happyfamily(name):
    print("%s : The program ---happy family--- is boring!!!" % name)


def eat_meat(name):
    print("%s : The meat is nice!!!" % name)


def eat_hamburger(name):
    print("%s : The hamburger is not so bad!!!" % name)


if __name__ == "__main__":
    a = [eat_hamburger, eat_meat]
    a[1]("dsaf")
    a[0]("dfaddfsdf")
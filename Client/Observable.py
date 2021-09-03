class Observable:
    def __init__(self):
        self._observers = []

    def notify(self, cmd, data=None):
        """
        Notify all observers.
        :param cmd: Identify by protocol with (command)
        :return: None.
        """
        for observer in self._observers:
            observer.update(cmd, data)

    def attach(self, observer):
        """
        Attach Observer to Observable object.
        :param observer: Observer object
        :return: None.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detach Observer from Observable object.
        :param observer: Observer object
        :return: None
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

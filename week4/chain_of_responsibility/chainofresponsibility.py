import logging


logging.basicConfig(level=logging.INFO)


class SomeObject:

    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:

    def __init__(self, type):
        self.type = type


class EventSet:

    def __init__(self, value):
        self.value = value


class NullHandler:

    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
            return self.successor.handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == str:
            return obj.string_field
        elif (isinstance(event, EventSet) and
              isinstance(event.value, str)):
            obj.string_field = event.value
        else:
            return self.successor.handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == float:
            return obj.float_field
        elif (isinstance(event, EventSet) and
              isinstance(event.value, float)):
            obj.float_field = event.value
        else:
            return self.successor.handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type == int:
            return obj.integer_field
        elif (isinstance(event, EventSet) and
              isinstance(event.value, int)):
            obj.integer_field = event.value
        else:
            return self.successor.handle(obj, event)


# Testing
if __name__ == '__main__':
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"

    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
    logging.info('Get event: int')
    print(chain.handle(obj, EventGet(int)))
    logging.info('Get event: float')
    print(chain.handle(obj, EventGet(float)))
    logging.info('Get event: str')
    print(chain.handle(obj, EventGet(str)))
    logging.info('Set event: 100')
    print(chain.handle(obj, EventSet(100)))
    logging.info('Set event: 0.5')
    print(chain.handle(obj, EventSet(0.5)))
    logging.info('Get event: float')
    print(chain.handle(obj, EventGet(float)))
    logging.info('Set event: new text')
    print(chain.handle(obj, EventSet('new text')))
    logging.info('Get event: str')
    print(chain.handle(obj, EventGet(str)))

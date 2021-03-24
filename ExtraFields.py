from itertools import islice


class ExtraData:

    def __init__(self):
        self.extra_data_storage = {}
        self.counter_dict = {}

    def counter_handler(self, key):
        if key not in self.counter_dict:
            self.counter_dict[key] = 1

    def increment_element_number(self, key):
        self.counter_dict[key] = self.counter_dict[key] + 1

    def extra_data_handler(self, event, key_name):
        self.counter_handler(key_name)

        for event_num in range(len(event)):

            if event[event_num] is None:
                event[event_num] = 'none'

            if key_name + '.' + str(self.counter_dict[key_name]) not in self.extra_data_storage:
                self.extra_data_storage[key_name + '.' + str(self.counter_dict[key_name])] = event[event_num]
            else:
                if len(str(self.extra_data_storage[key_name + '.' + str(self.counter_dict[key_name])]) + str(
                        ',' + event[event_num])) < 1024:
                    self.extra_data_storage[key_name + '.' + str(self.counter_dict[key_name])] += ',' + event[event_num]
                else:
                    self.increment_element_number(key_name)
                    self.extra_data_storage[key_name + '.' + str(self.counter_dict[key_name])] = event[event_num]

    def take(self, n):
        slice_dict = islice(self.extra_data_storage.items(), n)
        return dict(slice_dict)

    def remove_dups(self, dict1):
        for k in dict1:
            self.extra_data_storage.pop(k, None)

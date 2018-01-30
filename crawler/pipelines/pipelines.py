import json
import logging

logger = logging.getLogger(__name__)

'''
A pipeline write data to file

@example
    yield {
        '_file': 'data.json',
        '_mode': 'a'
    }
'''
class FilePipeline(object):

    def open_spider(self, spider):
        self.files = {}
        self.logger = logger

    def process_item(self, item, spider):
        data = item.copy()
        name = data.pop('_file', None)
        mode = data.pop('_mode', 'w')

        '''
        Check for valid pipeline item
        '''
        if not name:
            return item

        '''
        Remove all helper keys with format: _{key}
        '''
        for k in data.keys():
            if '_' in k:
                data.pop(k)

        '''
        Get file writer handle
        '''
        writer = None

        if name not in self.files:
            self.files[name] = writer = open(name, mode)
        else:
            writer = self.files[name]

        line = json.dumps(dict(data)) + "\n"

        '''
        Write data to file
        '''
        writer.write(line)
        writer.flush()

        return item

    def close_spider(self, spider):
        for _, x in self.files.items():
            x.close()


# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import os
import boto
import ConfigParser
from boto.utils import find_class

class Startup:

    def read_metadata(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(os.path.expanduser('~pyami/metadata.ini'))

    def get_instance_data(self, name):
        try:
            val = self.config.get('Metadata', name)
        except:
            val = None
        return val

    def get_user_data(self, name):
        try:
            val = self.config.get('Userdata', name)
        except:
            val = None
        return val

    def get_script(self):
        script_name = self.get_user_data('script_name')
        if script_name:
            c = boto.connect_s3(self.get_user_data('aws_access_key_id'),
                                self.get_user_data('aws_secret_access_key'))
            script_name = script + '.py'
            bucket = c.get_bucket(self.get_user_data('bucket_name'))
            script = bucket.get_key(script_name)
            print 'Fetching %s.%s' % (bucket.name, script.name)
            script_path = os.path.join(self.working_dir, script_name)
            script.get_contents_to_filename(script_path)
            self.module_name = script_name
        else:
            self.module_name = self.get_user_data('module_name')

    def run_script(self):
        if self.module_name:
            cls = find_class(self.module_name,
                             self.get_user_data('class_name'))
        s = cls(self.config)
        s.run()

    def main(self):
        self.read_metadata()
        self.get_script()
        self.run_script()

if __name__ == "__main__":
    su = Startup()
    su.main()
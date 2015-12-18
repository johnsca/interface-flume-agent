# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class FlumeProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.GLOBAL
    relation_name = 'flume-agent'

    def __init__(self, port=None, protocol='avro', **args):
        self.flume_protocol = protocol
        self.port = port  # only needed for provides
        super(FlumeProvides, self).__init__(FlumeProvides.relation_name, **args)

    # Use some template magic to declare our relation(s)
    @hook('{provides:flume-agent}-relation-{joined,changed}')
    def changed(self):
        self.configure(self.flume_protocol)
        self.set_state('{relation_name}.available')

    @hook('{provides:flume-agent}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    # call this method when passed into methods decorated with
    # @when('{relation}.available')
    # to configure the relation data
    def configure(self, protocol):
        if (protocol not in ['avro']):
            return False
        
        self.flume_protocol = protocol
        relation_info = {
            'port': self.port,
            'protocol': self.flume_protocol,
        }
        self.set_remote(**relation_info)


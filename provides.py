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

    # Use some template magic to declare our relation(s)
    @hook('{provides:flume-agent}-relation-joined')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:flume-agent}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:flume-agent}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    # call this method when passed into methods decorated with
    # @when('{relation}.available')
    # to configure the relation data
    def send_configuration(self, port, protocol = 'avro'):
        if (protocol not in ['avro']):
            return False
        
        conv = self.conversation()
        conv.set_remote(data = {
            'port': port,
            'protocol': protocol,
        })
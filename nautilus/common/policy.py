# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import functools

from oslo_config import cfg
from oslo_policy import policy

from nautilus.common import policies
from nautilus import exceptions as n_exc


CONF = cfg.CONF
_ENFORCER = None


def setup_policy():
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        register_rules(_ENFORCER)


def enforce(rule):

    setup_policy()

    def decorator(func):
        @functools.wraps(func)
        def handler(*args, **kwargs):
            context = args[1].context
            _ENFORCER.enforce(rule, {}, context.to_dict(),
                              do_raise=True,
                              exc=n_exc.ActionForbidden)
            return func(*args, **kwargs)
        return handler

    return decorator


def register_rules(enforcer):
    enforcer.register_defaults(policies.list_rules())

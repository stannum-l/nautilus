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

import falcon
from oslo_log import log

from nautilus.common.i18n import _


LOG = log.getLogger(__name__)


class NautilusException(falcon.HTTPError):
    status = falcon.HTTP_500
    message = "unknown error"
    title = "Internal Server Error"

    def __init__(self, message=None, **kwargs):
        self.message = message or self.message
        super(NautilusException, self).__init__(
            self.status, self.title, self.message, **kwargs
        )


class ActionForbidden(NautilusException):
    status = falcon.HTTP_403
    message = _("Insufficient privilege to perform action.")
    title = _("Action Forbidden")


class JSONException(NautilusException):
    status = falcon.HTTP_NOT_ACCEPTABLE


class APIException(NautilusException):
    status = falcon.HTTP_400

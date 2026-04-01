#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import Optional

from ariadne_codegen import Plugin

now = datetime.now()

license = f"""#  Copyright {now.year} Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

class LicenseHeadersPlugin(Plugin):

    def get_file_comment(
        self, comment: str, code: str, source: Optional[str] = None
    ) -> str:
        return f"{license}{comment}"

    def copy_code(self, copied_code: str) -> str:
        return f"{license}\n\n{copied_code}"

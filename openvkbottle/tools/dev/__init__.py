import sys
import warnings

warnings.warn(
    "Imports from openvkbottle.tools.dev is deprecated, use openvkbottle.tools instead",
    FutureWarning,
    stacklevel=0,
)

sys.modules["openvkbottle.tools.dev"] = sys.modules["openvkbottle.tools"]

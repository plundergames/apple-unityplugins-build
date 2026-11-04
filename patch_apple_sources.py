"""Small changes to Apple's sources before building. Fails if the sources no longer match."""
import pathlib
import re
import sys

CORE = pathlib.Path("plug-ins/Apple.Core/Apple.Core_Unity/Assets/Apple.Core")
GAMEKIT = pathlib.Path("plug-ins/Apple.GameKit/Apple.GameKit_Unity/Assets/Apple.GameKit")

# Startup hooks that call native libraries. Those do not exist in a Windows Editor, where the hooks
# would log a DllNotFoundException at every Play Mode start.
STARTUP_HOOKS = {
    CORE / "Runtime/Availability.cs": 1,
    GAMEKIT / "Source/DefaultHandlers.cs": 2,
    GAMEKIT / "Source/GKGameActivity.cs": 1,
}
HOOK = re.compile(r"^([ \t]*\[(?:UnityEngine\.)?RuntimeInitializeOnLoadMethod[^\r\n]*\][ \t]*)(\r?\n)", re.M)

# In batch mode Apple waits only 5 seconds for the package list; on a miss the frameworks are not
# embedded and the build fails at the end of Xcode. .Seconds also wraps every minute.
ENVIRONMENT = CORE / "Editor/ApplePlugInEnvironment.cs"
REPLACEMENTS = (
    ("_packageManagerBatchModeListRequestTimeout => 5;", "_packageManagerBatchModeListRequestTimeout => 120;"),
    ("(DateTime.Now - startTime).Seconds >", "(DateTime.Now - startTime).TotalSeconds >"),
)


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


for path, expected in STARTUP_HOOKS.items():
    text, count = HOOK.subn(r"#if !UNITY_EDITOR_WIN\2\1\2#endif\2", read(path))
    if count != expected:
        sys.exit(f"{path}: expected {expected} startup hooks, found {count}")
    write(path, text)

text = read(ENVIRONMENT)
for old, new in REPLACEMENTS:
    if text.count(old) != 1:
        sys.exit(f"{ENVIRONMENT}: expected exactly one '{old}'")
    text = text.replace(old, new)
write(ENVIRONMENT, text)
print("Patched Apple sources.")

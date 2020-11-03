import shlex
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_call
from typing import Final, Optional, Sequence

IMG_EXTS: Final[Sequence[str]] = (
    ".png",
    ".jpg",
    ".svg",
)


@dataclass
class Notification:
    """Message object encapsulating title, message, icon and display()."""

    title: str
    message: str
    icon: Optional[Path] = None
    duration: int = 0  # duration in milliseconds

    @staticmethod
    def check_icon_path(icon: Path) -> str:
        """Return absolute path if path exists and is image file."""
        if not icon.exists():
            raise ValueError(f"{icon} does not exist.")
        if not icon.is_file():
            raise ValueError(f"{icon} is not a file.")
        if icon.suffix not in IMG_EXTS:
            raise ValueError(f"{icon} is not an image file.")
        return str(icon.absolute())

    def display(self) -> None:
        """Display notification."""
        icon_cmd = f"-i {self.check_icon_path(self.icon)}" if self.icon else ""
        msg_cmd = f"'{self.message}'" if self.message else ""
        duration_cmd = f"-t {self.duration}" if self.duration else ""
        cmd = f"notify-send '{self.title}' {icon_cmd} {msg_cmd} {duration_cmd}"
        check_call(shlex.split(cmd))

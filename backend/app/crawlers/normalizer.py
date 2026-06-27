import re
import unicodedata
from dataclasses import dataclass

PLATFORM_SUFFIX_RE = re.compile(
    r"(\s*(?:[-–—]\s*)?(?:\((?:pc|steam|windows|mac|linux)\)|pc|steam|windows|mac|linux))+$",
    re.IGNORECASE,
)
WHITESPACE_RE = re.compile(r"\s+")
SLUG_SEPARATOR_RE = re.compile(r"[^a-z0-9]+")
SLUG_TRIM_RE = re.compile(r"^-+|-+$")
TRAILING_SEPARATOR_RE = re.compile(r"[\s\-–—:|/]+$")


@dataclass(frozen=True)
class NormalizedGameTitle:
    canonical_name: str
    slug: str


def normalize_title(raw_title: str) -> str:
    title = raw_title.replace("™", "").replace("®", "")
    title = PLATFORM_SUFFIX_RE.sub("", title)
    title = TRAILING_SEPARATOR_RE.sub("", title)
    title = WHITESPACE_RE.sub(" ", title)

    return title.strip().lower()


def generate_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = SLUG_SEPARATOR_RE.sub("-", ascii_value.lower())

    return SLUG_TRIM_RE.sub("", slug)


def normalize_game_title(raw_title: str) -> NormalizedGameTitle:
    canonical_name = normalize_title(raw_title)

    return NormalizedGameTitle(
        canonical_name=canonical_name,
        slug=generate_slug(canonical_name),
    )

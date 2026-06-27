import pytest

from app.crawlers import generate_slug, normalize_game_title, normalize_title


@pytest.mark.parametrize(
    ("raw_title", "canonical_name"),
    [
        ("Cyberpunk 2077™", "cyberpunk 2077"),
        ("Cyberpunk 2077 - PC", "cyberpunk 2077"),
        ("Cyberpunk 2077 (Steam)", "cyberpunk 2077"),
        ("  Cyberpunk   2077®   ", "cyberpunk 2077"),
        ("Hades II — Windows", "hades ii"),
        ("Portal 2 Steam PC", "portal 2"),
    ],
)
def test_normalize_title_generates_canonical_name(
    raw_title: str,
    canonical_name: str,
) -> None:
    assert normalize_title(raw_title) == canonical_name


@pytest.mark.parametrize(
    ("value", "slug"),
    [
        ("cyberpunk 2077", "cyberpunk-2077"),
        ("Sid Meier's Civilization VII", "sid-meier-s-civilization-vii"),
        ("Ação & Aventura: Edição Completa", "acao-aventura-edicao-completa"),
        ("  multiple   spaces  ", "multiple-spaces"),
    ],
)
def test_generate_slug_is_url_friendly(value: str, slug: str) -> None:
    assert generate_slug(value) == slug


def test_normalize_game_title_returns_canonical_name_and_slug() -> None:
    normalized = normalize_game_title("Cyberpunk 2077™ - PC")

    assert normalized.canonical_name == "cyberpunk 2077"
    assert normalized.slug == "cyberpunk-2077"

from ihq._cli import render_examples


def test_aligns_comment_column_to_longest_command() -> None:
    rendered = render_examples([("ab", "x"), ("abcd", "y")])

    assert rendered == (
        "  [cyan]ab[/cyan]    [dim]# x[/dim]\n  [cyan]abcd[/cyan]  [dim]# y[/dim]"
    )


def test_single_example_uses_two_space_gap() -> None:
    rendered = render_examples([("ihq list", "Show this repo's managed paths")])

    assert rendered == (
        "  [cyan]ihq list[/cyan]  [dim]# Show this repo's managed paths[/dim]"
    )

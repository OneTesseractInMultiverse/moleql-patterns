def test_package_imports() -> None:
    import moleql_patterns

    assert isinstance(moleql_patterns.__version__, str)

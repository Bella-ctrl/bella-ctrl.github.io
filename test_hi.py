from hi import hello

def test_default():
    assert hello() == "Hello, world"

def test_argument():
    for name in ["Alice", "Bob", "Charlie"]:
        assert hello(name) == f"Hello, {name}"

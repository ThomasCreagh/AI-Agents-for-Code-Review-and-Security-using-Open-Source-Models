from git_analyser import print_hello_world


def test_run():
    assert print_hello_world.run() == "hello world"

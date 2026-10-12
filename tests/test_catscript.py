import sys
from pathlib import Path
from unittest.mock import patch
import pytest

# Ensure parent directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from catscript import run_catscript


@pytest.fixture(autouse=True)
def mock_cat_sleep():
    """Mock time.sleep to run the test suite instantly without 5ms/5s delays."""
    with patch("time.sleep", return_value=None):
        yield


def test_hello_cat_example(capsys, tmp_path):
    """Verifies that examples/hello.cat successfully outputs 'Hello'."""
    hello_file = Path(__file__).resolve().parent.parent / "examples" / "hello.cat"
    run_catscript(str(hello_file))
    captured = capsys.readouterr()
    assert captured.out == "Hello"


def test_basic_math_operations(capsys, tmp_path):
    """Tests Meow, Hiss, Tygydyk, Churu, Share, and Scream."""
    script = tmp_path / "math_test.cat"
    script.write_text(
        "; Test basic math\n"
        "Meow\n"              # belly = 1
        "MeowMeowMeow\n"      # belly = 11
        "Hiss\n"              # belly = 10
        "Tygydyk\n"           # belly = 20
        "Share\n"             # belly = 10
        "Churu\n"             # belly = 50
        "Scream\n",
        encoding="utf-8"
    )
    run_catscript(str(script))
    captured = capsys.readouterr()
    assert "[Belly Value]: 50" in captured.out


def test_memory_burry_and_digout(capsys, tmp_path):
    """Tests saving and retrieving treats from memory."""
    script = tmp_path / "memory_test.cat"
    script.write_text(
        "MeowMeowMeow\n"  # belly = 10
        "Burry\n"         # memory = 10
        "Drop\n"          # belly = 0
        "DigOut\n"        # belly = 10
        "Scream\n",
        encoding="utf-8"
    )
    run_catscript(str(script))
    captured = capsys.readouterr()
    assert "[Belly Value]: 10" in captured.out


def test_loops_tailup_taildown(capsys, tmp_path):
    """Tests countdown loop with TailUp and TailDown."""
    script = tmp_path / "loop_test.cat"
    script.write_text(
        "; Loop 3 times\n"
        "Meow\n"
        "Meow\n"
        "Meow\n"        # belly = 3
        "TailUp\n"
        "Hiss\n"        # decrement
        "TailDown\n"
        "Scream\n",     # belly should be 0
        encoding="utf-8"
    )
    run_catscript(str(script))
    captured = capsys.readouterr()
    assert "[Belly Value]: 0" in captured.out


def test_bite_stops_gracefully(tmp_path):
    """Tests that Bite gracefully stops the program with sys.exit(0)."""
    script = tmp_path / "bite_test.cat"
    script.write_text("Bite\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        run_catscript(str(script))
    assert exc_info.value.code == 0


def test_file_not_found(capsys):
    """Verifies clean handling when a file does not exist."""
    run_catscript("non_existent_cat.cat")
    captured = capsys.readouterr()
    assert "[Error]: File 'non_existent_cat.cat' not found!" in captured.out

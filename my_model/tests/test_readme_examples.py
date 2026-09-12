"""Executes every python code block in README.md, in document order and in
one shared namespace (matching how a reader follows the document), to prove
the documented usage examples actually work against the current public
interface.
"""

import re
from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent / "README.md"
CODE_BLOCK_PATTERN = re.compile(r"```python\n(.*?)```", re.DOTALL)


def _readme_code_blocks() -> list[str]:
    text = README_PATH.read_text(encoding="utf-8")
    return CODE_BLOCK_PATTERN.findall(text)


def test_every_readme_example_runs_successfully_in_document_order() -> None:
    namespace: dict[str, object] = {}
    for index, code in enumerate(_readme_code_blocks()):
        exec(compile(code, f"README.md:block-{index}", "exec"), namespace)  # noqa: S102


def test_readme_has_at_least_one_example_per_required_topic() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    required_topics = [
        "model_dump(",
        "model_dump_json(",
        "model_json_schema(",
        "ValidationError",
        "model_copy(update=",
        "credential",
    ]
    for topic in required_topics:
        assert topic in text, f"README.md is missing an example covering {topic!r}"

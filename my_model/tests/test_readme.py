import re
from pathlib import Path

import my_model

README_PATH = Path(__file__).resolve().parent.parent / "README.md"

REQUIRED_TOPICS = [
    "What this package owns",
    "What this package does not own",
    "Installation and import",
    "Public interface and usage pattern",
    "Model categories",
    "Boundary with other Components",
    "Validation, serialization, credential, and extension rules",
]

REQUIRED_EXAMPLE_SCENARIOS = [
    "Import the package namespace and use its module-qualified interface",
    "Import one public Model module directly",
    "Construct a valid Model instance",
    "Observe and handle a validation failure",
    "Serialize an instance to a dict and to JSON",
    "Generate a Model's JSON Schema",
    "Distinguish omitted, explicit-null, supplied, default, and generated values",
    "Perform a partial update that preserves the documented update semantics",
    "Use a reusable type and a declared relationship",
    "Handle a sensitive or credential field without exposing its protected value",
]

CODE_FENCE_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)

REAL_DOMAIN_MODEL_NAMES = [name for name in my_model.__all__ if name[:1].isupper()]


def _readme_text() -> str:
    return README_PATH.read_text()


def test_readme_exists_at_package_boundary() -> None:
    assert README_PATH.is_file()


def test_readme_covers_every_required_topic() -> None:
    text = _readme_text()
    for topic in REQUIRED_TOPICS:
        assert topic in text, f"README is missing required topic: {topic}"


def test_readme_covers_every_required_example_scenario() -> None:
    text = _readme_text()
    for scenario in REQUIRED_EXAMPLE_SCENARIOS:
        assert scenario in text, f"README is missing required example scenario: {scenario}"


def test_readme_examples_are_domain_neutral() -> None:
    text = _readme_text()
    for real_model_name in REAL_DOMAIN_MODEL_NAMES:
        assert real_model_name not in text, (
            f"README names the project-specific Model '{real_model_name}'; "
            "examples must stay domain-neutral"
        )


def test_readme_python_examples_all_execute_successfully() -> None:
    code_blocks = CODE_FENCE_RE.findall(_readme_text())
    assert len(code_blocks) >= len(REQUIRED_EXAMPLE_SCENARIOS)
    for index, block in enumerate(code_blocks, start=1):
        namespace: dict[str, object] = {}
        try:
            exec(compile(block, f"<readme example {index}>", "exec"), namespace)
        except Exception as error:  # pragma: no cover - failure path
            raise AssertionError(
                f"README example {index} raised {type(error).__name__}: {error}\n---\n{block}"
            ) from error

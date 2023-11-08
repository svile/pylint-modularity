# pylint-import-restriction

Pylint plugin to help enforce separation of concerns through import restrictions.

## Installation

Install the module with e.g. `poetry add --group dev pylint_import_restriction`.

## Usage
In your Pylint configuration (e.g. in `pyproject.toml`) add the following:
```
[tool.pylint.MAIN]
load-plugins = "pylint_import_restriction"
import-restriction="module_visited->module_import_restriction;module2_visited->restriction\\..*"
```
The restrictions configured as part of `import-restriction` setting, and as represented above take the following shape - `module_visited -> import_restriction`
- `module_visited`: is the module which is presently being looked at. This could be a RegEx in order to capture several modules.
- `import_restriction`:

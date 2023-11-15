import astroid
from astroid.builder import AstroidBuilder
from pylint.interfaces import UNDEFINED
import pylint.testutils
import pylint_import_restriction


class TestChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint_import_restriction.ImportRestriction
    CONFIG: dict[str, list[str]] = {
        "import-restriction": ["module.* -> .*restricted.*"]
    }

    def test_import_restriction(self) -> None:
        import_node = astroid.extract_node(
            """
            import restricted_one
            """,
            module_name="module.under.test",
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="import-restriction",
                line=2,
                node=import_node,
                args=("restricted_one", "module.under.test"),
                confidence=UNDEFINED,
                col_offset=0,
                end_line=2,
                end_col_offset=21,
            ),
        ):
            self.checker._current_module = "module.under.test"
            self.checker.visit_import(import_node)

    def test_from_import_restriction(self) -> None:
        import_node = astroid.extract_node(
            """
            from restricted import module
            """,
            module_name="module.under.test",
        )
        result_message = pylint.testutils.MessageTest(
            msg_id="import-restriction",
            line=2,
            node=import_node,
            args=("restricted.module", "module.under.test"),
            confidence=UNDEFINED,
            col_offset=0,
            end_line=2,
            end_col_offset=29,
        )
        with self.assertAddsMessages(result_message, result_message):
            self.checker._current_module = "module.under.test"
            self.checker.visit_importfrom(import_node)

    def test_from_relative_import_restriction(self) -> None:
        import_node = astroid.extract_node(
            """
            from ..restricted import some_module
            """,
            module_name="module.under.test",
        )
        result_message = pylint.testutils.MessageTest(
            msg_id="import-restriction",
            line=2,
            node=import_node,
            args=("module.restricted.some_module", "module.under.test"),
            confidence=UNDEFINED,
            col_offset=0,
            end_line=2,
            end_col_offset=36,
        )
        with self.assertAddsMessages(result_message, result_message, result_message):
            self.checker._current_module = "module.under.test"
            self.checker.visit_importfrom(import_node)

    def test_import_non_restriction(self) -> None:
        import_node = astroid.extract_node(
            """
            import non_valid_module
            """,
            module_name="module.under.test",
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_free_module(self) -> None:
        import_node = astroid.extract_node(
            """
            import free_valid_module
            """,
            module_name="module.under.test",
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_visit_module(self) -> None:
        import_node = AstroidBuilder().string_build(
            "import some_module",
            modname="some.module.under.test",
        )
        with self.assertNoMessages():
            self.checker.visit_module(import_node)
        assert self.checker._current_module == "some.module.under.test"

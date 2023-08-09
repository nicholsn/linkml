from typing import Iterator

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


class RecommendedSlotsPlugin(ValidationPlugin):
    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        def _do_process(
            instance: dict, class_name: str, location: str
        ) -> Iterator[ValidationResult]:
            if not isinstance(instance, dict):
                return
            for slot_def in context.schema_view.class_induced_slots(class_name):
                slot_value = instance.get(slot_def.name, None)
                if slot_def.recommended and slot_value is None:
                    yield ValidationResult(
                        type="recommended slots",
                        severity=Severity.WARN,
                        instance=instance,
                        instantiates=class_name,
                        message=f"Slot '{slot_def.name}' is recommended on class '{class_name}' in {location}",
                    )
                slot_range_class = context.schema_view.get_class(slot_def.range)
                if slot_range_class is not None and slot_value is not None:
                    location += f".{slot_def.name}"
                    if slot_def.multivalued:
                        if slot_def.inlined and isinstance(slot_value, dict):
                            for k, v in slot_value.items():
                                yield from _do_process(v, slot_range_class.name, location + f".{k}")
                        elif slot_def.inlined_as_list and isinstance(slot_value, list):
                            for i, v in enumerate(slot_value):
                                yield from _do_process(
                                    v, slot_range_class.name, location + f"[{i}]"
                                )
                    else:
                        yield from _do_process(
                            instance[slot_def.name], slot_range_class.name, location
                        )

        yield from _do_process(instance, context.target_class, "$")

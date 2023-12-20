import dataclasses
from dataclasses import dataclass, _MISSING_TYPE
from munch import Munch

DTO_REQUIRED = "___REQUIRED___"

# pylint: disable=invalid-field-call
def nested_dto(x, raw=False):
    return dataclasses.field(default_factory=lambda: x if raw else Munch.fromDict(x))

@dataclass(frozen=True)
class BaseDTO:
    def __new__(cls, **kwargs):
        setteable_fields = cls.setteable_fields()
        mandatory_fields = cls.mandatory_fields()
        invalid_kwargs = [
            {k: v} for k, v in kwargs.items() if k not in setteable_fields or v == DTO_REQUIRED
        ]
        assert (
            len(invalid_kwargs) == 0
        ), f"Invalid fields detected when initializing this DTO: {invalid_kwargs}.\nDeclare this field and set it to None or DTO_REQUIRED in order to make it setteable."
        missing_kwargs = [f for f in mandatory_fields if f not in kwargs]
        assert (
            len(missing_kwargs) == 0
        ), f"Required fields missing initializing this DTO: {missing_kwargs}."
        return object.__new__(cls)
        

    @classmethod
    def setteable_fields(cls):
        return [f.name for f in dataclasses.fields(cls) if f.default is None or isinstance(f.default, _MISSING_TYPE) or f.default == DTO_REQUIRED]

    @classmethod
    def mandatory_fields(cls):
        return [f.name for f in dataclasses.fields(cls) if isinstance(f.default, _MISSING_TYPE) and isinstance(f.default_factory, _MISSING_TYPE) or f.default == DTO_REQUIRED]

    @classmethod
    def from_dict(cls, kwargs):
        for k in kwargs:
            if isinstance(kwargs[k], (dict, list, tuple)):
                kwargs[k] = Munch.fromDict(kwargs[k])
        return cls(**kwargs)

    def to_dict(self):
        # selfdict = dataclasses.asdict(self) # needs to pickle stuff, doesn't support some more complex classes
        selfdict = {}
        for k in dataclasses.fields(self):
            selfdict[k.name] = getattr(self, k.name)
            if isinstance(selfdict[k.name], Munch):
                selfdict[k.name] = selfdict[k.name].toDict()
        return selfdict

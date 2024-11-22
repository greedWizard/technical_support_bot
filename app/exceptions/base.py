from dataclasses import asdict, dataclass


@dataclass(frozen=True, eq=False)
class ApplicationException(Exception):
    @property
    def meta(self) -> dict:
        return asdict(self)

    @property
    def message(self) -> str:
        return 'В работе приложения произошла ошибка'

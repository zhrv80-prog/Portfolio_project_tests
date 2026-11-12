from dataclasses import dataclass, asdict

# --- Модель данных ---
@dataclass
class User:
    firstName: str
    lastName: str
    email: str
    password: str

    def to_dict(self) -> dict:
        return asdict(self)

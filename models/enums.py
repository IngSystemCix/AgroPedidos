import enum

class PaymentMethod(enum.Enum):
    D = "D"   # Débito‑crédito
    Y = "Y"   # Yape

class NotificationStatus(enum.Enum):
    S = "S"   # Success
    E = "E"   # Error
    P = "P"   # Pending

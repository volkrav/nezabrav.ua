from enum import EnumMeta, Enum
from pydantic import BaseModel


class STracking(BaseModel):
    Number: str # Номер документу (ЕН)
    DateCreated: str | None # Дата створення ЕН "08-09-2023 18:05:35"
    PhoneRecipient:	str | None	# Номер телефону отримувача
    CityRecipient: str | None # Місто отримувача
    WarehouseRecipient: str | None # Склад отримувача
    DocumentCost: str | None # Вартість доставки
    StoragePrice: str | None # Вартість зберігання

    class Config:
        from_attributes = True
        populate_by_name = True


class SAddReport(BaseModel):
    phone: str
    first_name: str | None = None
    last_name: str
    ttn: str
    report: str | None

    class Config:
        from_attributes = True


class MyMeta(EnumMeta):
    def __contains__(self, other):
        try:
            self(other)
        except ValueError:
            return False
        else:
            return True

class EStatus(Enum, metaclass=MyMeta):
    refusal_to_receive = '102' # Відмова від отримання (Відправником створено замовлення на повернення)
    refusal = '103' # Відмова одержувача (отримувач відмовився від відправлення)
    forwarding = '104' # Змінено адресу
    storage_stopped = '105' # Припинено зберігання
    test = '7'
    test_ = '8'

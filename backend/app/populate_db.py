from hashlib import sha256

from core.database import engine
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from models.security_tip import SecurityTip
from sqlalchemy.orm import Session

# from models.password import Password


def populate_dummy_data():
    session = Session(bind=engine)
    data_type = session.query(DataType).first()
    if data_type is not None:
        session.close()
        return

    # IDEA: En la tabla intermedia que relaciona un Breach con un DataType, agregar una columna de display name.
    # Así podremos crear nombres customs y personalizados para cada breach, mantiendo el tipo de dato base.
    # Ej: Si en un breach se filtró el nombre completo y en otro solo el apellido (ambos son nombres), podemos
    # simplemente en un breach darle el display name de nombre completo, mientras que en el otro darle el display de apellido.

    # Initial DataTypes
    data_types: dict[str, DataType] = {
        "email": DataType(id=1, name="email", display_name="Correo electrónico"),
        "rut": DataType(id=2, name="rut", display_name="RUT"),
        "phone": DataType(id=3, name="phone", display_name="Número telefónico"),
        "credit_card": DataType(
            id=4, name="credit_card", display_name="Tarjeta de crédito"
        ),
        "address": DataType(id=5, name="address", display_name="Dirección"),
        "ip_address": DataType(id=6, name="ip_address", display_name="Dirección IP"),
        "name": DataType(id=7, name="name", display_name="Nombre"),
        "password": DataType(id=8, name="password", display_name="Contraseña"),
    }
    session.add_all(list(data_types.values()))
    session.commit()

    # Breaches
    breaches: list[Breach] = [
        Breach(
            id=1,
            name="Entel",
            description="El año 2022, Entel fue víctima de un hackeo masivo que afectó a más de 250.000 clientes. Filtrándose mucha información sensible de estos.",
            breach_date="2022-07-26",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["phone"],
                data_types["rut"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        Breach(
            id=2,
            name="Banco Estado",
            description="El año 2023, BancoEstado sufrió una filtración de su base de datos, que comprometió alrededor de 52.000 clientes.",
            breach_date="2023-11-08",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["password"],
                data_types["rut"],
                data_types["name"],
                data_types["credit_card"],
            ],
        ),
        Breach(
            id=3,
            name="Ripley",
            description="En el año 2022, Ripley publicó involuntariamente informacion de compras de 9.000 usuarios.",
            breach_date="2022-08-18",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["name"],
                data_types["address"],
                data_types["ip_address"],
            ],
        ),
    ]
    session.add_all(breaches)
    session.commit()
    # session.refresh(breaches)

    # DataLeaks
    data_leaks = [
        DataLeak(
            id=1,
            hash_value=sha256("nico@example.com".encode("UTF-8")).hexdigest(),
            data_type=data_types["email"],
            breach_id=2,
            found_with=[
                data_types["credit_card"],
                data_types["rut"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=2,
            hash_value=sha256("nico@example.com".encode("UTF-8")).hexdigest(),
            data_type=data_types["email"],
            breach_id=3,
            found_with=[
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=3,
            hash_value=sha256("965672517".encode("UTF-8")).hexdigest(),
            data_type=data_types["phone"],
            breach_id=1,
            found_with=[
                data_types["rut"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=4,
            hash_value=sha256("204438285".encode("UTF-8")).hexdigest(),
            data_type=data_types["rut"],
            breach_id=1,
            found_with=[
                data_types["email"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=5,
            hash_value=sha256("204438285".encode("UTF-8")).hexdigest(),
            data_type=data_types["rut"],
            breach_id=3,
            found_with=[
                data_types["email"],
                data_types["ip_address"],
                data_types["name"],
            ],
        ),
    ]
    session.add_all(data_leaks)
    session.commit()

    # Security Tips
    security_tips: list[SecurityTip] = [
        SecurityTip(
            data_type_id=data_types["email"].id,
            description="Manténgase atenta(o) a posibles correos electrónicos fraudulentos.",
        ),
        SecurityTip(
            data_type_id=data_types["phone"].id,
            description="Manténgase atenta(o) a posibles llamadas o mensajes de textos fraudulentos.",
        ),
        SecurityTip(
            data_type_id=data_types["password"].id,
            description="Cambie esta contraseña en todas las cuentas que la utilicen, y no vuelva a utilizar esta misma contraseña nuevamente.",
        ),
        SecurityTip(
            data_type_id=data_types["credit_card"].id,
            description="Bloqueé su tarjeta de crédito y/o avise al banco que es posible que su tarjeta haya sido comprometida por terceros.",
        ),
    ]
    session.add_all(security_tips)
    session.commit()

    # Se cierra conexión
    session.close()

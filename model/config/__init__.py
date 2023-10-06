from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationMailerConfig:
    from_name: str
    from_address: str

    admin_name: str
    admin_address: str

    dsn: str


@dataclass(frozen=True)
class AppConfig:
    notification_mailer: NotificationMailerConfig

    db_connection_url: str

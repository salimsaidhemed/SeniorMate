from datetime import UTC, datetime

from app.extensions import db


class OrganizationSettings(db.Model):
    __tablename__ = "organization_settings"

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255), nullable=True)
    app_display_name = db.Column(db.String(120), nullable=True)
    logo_object_key = db.Column(db.String(1024), nullable=True, unique=True)
    logo_file_name = db.Column(db.String(255), nullable=True)
    logo_mime_type = db.Column(db.String(100), nullable=True)
    logo_file_size = db.Column(db.BigInteger, nullable=True)
    primary_color = db.Column(db.String(7), nullable=True)
    secondary_color = db.Column(db.String(7), nullable=True)
    accent_color = db.Column(db.String(7), nullable=True)
    sidebar_color = db.Column(db.String(7), nullable=True)
    login_banner_text = db.Column(db.Text, nullable=True)
    footer_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "organization_name": self.organization_name,
            "app_display_name": self.app_display_name,
            "has_custom_logo": bool(self.logo_object_key),
            "logo_file_name": self.logo_file_name,
            "logo_mime_type": self.logo_mime_type,
            "logo_file_size": self.logo_file_size,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "accent_color": self.accent_color,
            "sidebar_color": self.sidebar_color,
            "login_banner_text": self.login_banner_text,
            "footer_text": self.footer_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

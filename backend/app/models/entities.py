from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import LabelMode, ProviderStatus, VersionType


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    versions: Mapped[list[Version]] = relationship(back_populates="project")


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    pixel_width: Mapped[int] = mapped_column(Integer, nullable=False)
    pixel_height: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )


class Version(Base):
    __tablename__ = "versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    parent_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("versions.id"), nullable=True, index=True
    )
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), nullable=False)
    version_type: Mapped[str] = mapped_column(
        String(30), default=VersionType.ORIGINAL, nullable=False
    )
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(200), nullable=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    generation_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )

    project: Mapped[Project] = relationship(back_populates="versions")
    asset: Mapped[Asset] = relationship()
    parent: Mapped[Version | None] = relationship(remote_side=[id], backref="children")


class ProviderRun(Base):
    __tablename__ = "provider_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    model: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_version_id: Mapped[str] = mapped_column(ForeignKey("versions.id"), nullable=False)
    output_version_id: Mapped[str | None] = mapped_column(ForeignKey("versions.id"), nullable=True)
    original_instruction: Mapped[str] = mapped_column(Text, nullable=False)
    final_provider_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=ProviderStatus.QUEUED, nullable=False)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    run_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )


class Label(Base):
    __tablename__ = "labels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    version_id: Mapped[str] = mapped_column(ForeignKey("versions.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float | None] = mapped_column(Float, nullable=True)
    rotation: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    font_family: Mapped[str] = mapped_column(String(200), default="Arial", nullable=False)
    font_size: Mapped[float] = mapped_column(Float, default=16.0, nullable=False)
    alignment: Mapped[str] = mapped_column(String(20), default="left", nullable=False)
    mode: Mapped[str] = mapped_column(String(20), default=LabelMode.TEXT, nullable=False)
    style_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    version_id: Mapped[str] = mapped_column(ForeignKey("versions.id"), nullable=False, index=True)
    visual_quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    preferred: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )

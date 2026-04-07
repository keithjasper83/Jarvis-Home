from datetime import datetime, timezone
import uuid
from typing import Any, Dict, Optional

from sqlalchemy import String, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    deployment_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    friendly_name: Mapped[str] = mapped_column(String, nullable=False)
    canonical_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    device_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    vendor: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    room: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    protocol: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    host: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    auth_ref_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    adapter_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    health_state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc, onupdate=_now_utc)

class Capability(Base):
    __tablename__ = "capabilities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    capability_key: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    safety_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parameter_schema_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ui_hints_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    voice_examples_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc, onupdate=_now_utc)

class CommandExecution(Base):
    __tablename__ = "command_executions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    correlation_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    source_interface: Mapped[str] = mapped_column(String)
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    turn_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    device_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    capability_id: Mapped[str] = mapped_column(String)
    adapter_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parameters_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    result_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc)

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String, index=True)
    turn_index: Mapped[int] = mapped_column(Integer)
    transcript_raw: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    transcript_normalized: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parsed_intent_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    clarification_required: Mapped[bool] = mapped_column(Boolean, default=False)
    executed_plan_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    response_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tts_run_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now_utc)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

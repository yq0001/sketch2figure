"""Initial metadata schema for Sketch2Figure."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "assets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("file_path", sa.String(length=1000), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("pixel_width", sa.Integer(), nullable=False),
        sa.Column("pixel_height", sa.Integer(), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_path"),
    )
    op.create_index("ix_assets_checksum_sha256", "assets", ["checksum_sha256"])
    op.create_table(
        "versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("parent_version_id", sa.String(length=36), nullable=True),
        sa.Column("asset_id", sa.String(length=36), nullable=False),
        sa.Column("version_type", sa.String(length=30), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=True),
        sa.Column("model", sa.String(length=200), nullable=True),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("generation_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"]),
        sa.ForeignKeyConstraint(["parent_version_id"], ["versions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_versions_parent_version_id", "versions", ["parent_version_id"])
    op.create_index("ix_versions_project_id", "versions", ["project_id"])
    op.create_table(
        "provider_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=200), nullable=True),
        sa.Column("source_version_id", sa.String(length=36), nullable=False),
        sa.Column("output_version_id", sa.String(length=36), nullable=True),
        sa.Column("original_instruction", sa.Text(), nullable=False),
        sa.Column("final_provider_prompt", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("run_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["output_version_id"], ["versions.id"]),
        sa.ForeignKeyConstraint(["source_version_id"], ["versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_provider_runs_provider", "provider_runs", ["provider"])
    op.create_table(
        "labels",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("width", sa.Float(), nullable=True),
        sa.Column("rotation", sa.Float(), nullable=False),
        sa.Column("font_family", sa.String(length=200), nullable=False),
        sa.Column("font_size", sa.Float(), nullable=False),
        sa.Column("alignment", sa.String(length=20), nullable=False),
        sa.Column("mode", sa.String(length=20), nullable=False),
        sa.Column("style_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["version_id"], ["versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_labels_version_id", "labels", ["version_id"])
    op.create_table(
        "ratings",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("visual_quality_score", sa.Integer(), nullable=False),
        sa.Column("preferred", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["version_id"], ["versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ratings_version_id", "ratings", ["version_id"])


def downgrade() -> None:
    op.drop_index("ix_ratings_version_id", table_name="ratings")
    op.drop_table("ratings")
    op.drop_index("ix_labels_version_id", table_name="labels")
    op.drop_table("labels")
    op.drop_index("ix_provider_runs_provider", table_name="provider_runs")
    op.drop_table("provider_runs")
    op.drop_index("ix_versions_project_id", table_name="versions")
    op.drop_index("ix_versions_parent_version_id", table_name="versions")
    op.drop_table("versions")
    op.drop_index("ix_assets_checksum_sha256", table_name="assets")
    op.drop_table("assets")
    op.drop_table("projects")

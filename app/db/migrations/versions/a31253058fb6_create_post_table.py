"""create_post_table

Revision ID: a31253058fb6
Revises: 6d5ebb85f6c1
Create Date: 2023-12-26 10:44:00.005421

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a31253058fb6'
down_revision = '6d5ebb85f6c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Adiciona o trigger após criar a tabela
    op.execute("""
        CREATE OR REPLACE FUNCTION update_last_post()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE "user"
            SET last_post = NEW.created_at
            WHERE id = NEW.user_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER update_user_last_post
        AFTER INSERT
        ON post
        FOR EACH ROW
        EXECUTE FUNCTION update_last_post();
    """)

def downgrade() -> None:
    # Remove o trigger antes de excluir a tabela
    op.execute("""
        DROP TRIGGER IF EXISTS update_user_last_post ON post;
        DROP FUNCTION IF EXISTS update_last_post();
    """)

    op.drop_table("post")
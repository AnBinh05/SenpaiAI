"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_jlpt_level', sa.String(), nullable=True),
        sa.Column('learning_goals', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create chat_history table
    op.create_table('chat_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('jlpt_level', sa.String(), nullable=True),
        sa.Column('grammar_points', sa.JSON(), nullable=True),
        sa.Column('translation', sa.Text(), nullable=True),
        sa.Column('sources', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_history_id'), 'chat_history', ['id'], unique=False)

    # Create learning_sessions table
    op.create_table('learning_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_type', sa.String(), nullable=False),
        sa.Column('topic', sa.String(), nullable=True),
        sa.Column('difficulty_level', sa.String(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('questions_answered', sa.Integer(), nullable=True),
        sa.Column('correct_answers', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_sessions_id'), 'learning_sessions', ['id'], unique=False)

    # Create documents table
    op.create_table('documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('document_type', sa.String(), nullable=False),
        sa.Column('jlpt_level', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('embedding_id', sa.String(), nullable=True),
        sa.Column('chunk_index', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)

    # Create grammar_rules table
    op.create_table('grammar_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rule_name', sa.String(), nullable=False),
        sa.Column('japanese_pattern', sa.String(), nullable=False),
        sa.Column('meaning', sa.Text(), nullable=False),
        sa.Column('usage_notes', sa.Text(), nullable=True),
        sa.Column('examples', sa.JSON(), nullable=True),
        sa.Column('jlpt_level', sa.String(), nullable=False),
        sa.Column('difficulty_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grammar_rules_id'), 'grammar_rules', ['id'], unique=False)

    # Create vocabulary table
    op.create_table('vocabulary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('japanese_word', sa.String(), nullable=False),
        sa.Column('reading', sa.String(), nullable=True),
        sa.Column('meaning', sa.Text(), nullable=False),
        sa.Column('part_of_speech', sa.String(), nullable=True),
        sa.Column('jlpt_level', sa.String(), nullable=False),
        sa.Column('example_sentences', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vocabulary_id'), 'vocabulary', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_vocabulary_id'), table_name='vocabulary')
    op.drop_table('vocabulary')
    op.drop_index(op.f('ix_grammar_rules_id'), table_name='grammar_rules')
    op.drop_table('grammar_rules')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')
    op.drop_index(op.f('ix_learning_sessions_id'), table_name='learning_sessions')
    op.drop_table('learning_sessions')
    op.drop_index(op.f('ix_chat_history_id'), table_name='chat_history')
    op.drop_table('chat_history')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')



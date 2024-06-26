"""Add schema for Quiz, Question, Option

Revision ID: a79e76fbe79f
Revises: 15508c484648
Create Date: 2024-05-16 11:13:46.165849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a79e76fbe79f'
down_revision = '15508c484648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_quiz_user_id'), ['user_id'], unique=False)

    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('option')
    op.drop_table('question')
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_quiz_user_id'))

    op.drop_table('quiz')
    # ### end Alembic commands ###

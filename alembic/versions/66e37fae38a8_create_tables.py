"""create tables

Revision ID: 66e37fae38a8
Revises: 
Create Date: 2022-05-28 18:39:15.644426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66e37fae38a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('created', sa.DateTime),
    )
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('number', sa.Integer, nullable=False),
        sa.Column('created', sa.DateTime),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'))
    )
    op.create_table(
        'answers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('created', sa.DateTime),
        sa.Column('correct', sa.Boolean),
        sa.Column('award', sa.Integer, default=0),
        sa.Column('question_id', sa.Integer, sa.ForeignKey('questions.id'))
    )
def downgrade():
    op.drop_table('courses')
    op.drop_table('questions')
    op.drop_table('answers')

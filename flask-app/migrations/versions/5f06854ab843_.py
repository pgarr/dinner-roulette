"""empty message

Revision ID: 5f06854ab843
Revises: df9a5905978f
Create Date: 2019-05-19 12:33:16.495981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f06854ab843'
down_revision = 'df9a5905978f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('waiting_recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(length=1000), nullable=True),
    sa.Column('preparation', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('waiting_recipe_ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('unit', sa.String(length=20), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['waiting_recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('recipe_detail')
    op.add_column('recipe', sa.Column('link', sa.String(length=1000), nullable=True))
    op.add_column('recipe', sa.Column('preparation', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'preparation')
    op.drop_column('recipe', 'link')
    op.create_table('recipe_detail',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('link', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('preparation', sa.TEXT(), nullable=True),
    sa.Column('recipe_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('waiting_recipe_ingredient')
    op.drop_table('waiting_recipe')
    # ### end Alembic commands ###

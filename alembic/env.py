import asyncio

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import async_engine_from_config


from alembic import context
'''
Para a posterioridade:
YOU NEED TO START MYSQL SERVER: 
sudo /etc/init.d/mysql start

[Descomentar e alterar o alembic.ini antes de rodar a primeira revision ]
file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(rev)s_%%(slug)s

[Lembra de iniciar o db:  sudo /etc/init.d/mysql start]
$ alembic revision --autogenerate -m "first" 
Se o comando acima estiver rodando migrations vazias, é necessário importar os models que devem virar migrations...

[https://forum.rasa.com/t/mysql-tracker-store-gives-error-varchar-requires-a-length-on-dialect-mysql/10486/2]
Caso esteja dando problema com VARCHAR não tendo legnth use link acima:

Para poder comparar tipo use:
[ compare_type=True em run_migration_online()]

[O comando abaixo roda as migrations no banco de dados!]
$ alembic upgrade head 
é necessário acessar as migrations e colocar quantos VARCHAR são suportados por cada coluna em String 

'''
# import os, sys

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
'''SYNC'''
config.set_main_option("sqlalchemy.url","mysql+pymysql://mauricio:123@localhost:3306/fastapi_playground")
''' Async'''
# config.set_main_option("sqlalchemy.url","mysql+aiomysql://mauricio:123@localhost:3306/fastapi_playground")
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from db.base import Base
target_metadata = Base.metadata
# Models que serão traduzidos em migrations
# import db.db_models
# from db.db_models import user_db_model

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # import db.db_models
    # from db.db_models import user_db_model


    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

'''SYNC'''
def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # import db.db_models
    # from db.db_models import user_db_model

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

'''ASYNC'''
# def do_run_migrations(connection):
#     context.configure(connection=connection, target_metadata=target_metadata)

#     with context.begin_transaction():
#         context.run_migrations()

# async def run_migrations_online():
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = async_engine_from_config(
#         config.get_section(config.config_ini_section),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)

#     await connectable.dispose()



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

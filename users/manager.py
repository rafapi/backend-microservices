from main import app, db_u
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


migrate = Migrate(app, db_u)

manager = Manager(app)
manager.add_command('db_u', MigrateCommand)


if __name__ == '__main__':
    manager.run()

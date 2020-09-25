import os,click
from dotenv import load_dotenv
from app import create_app, db
from app.models import User,Role,Permission,Post,Follow,Comment
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

load_dotenv()
app = create_app(os.getenv('RLOG_CONFIG'))
manager = Manager(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Follow=Follow,Role=Role,Permission=Permission,Post=Post,Comment=Comment)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()



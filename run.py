from app import app
from app.models import User, Post, db, Product

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Product': Product}

if __name__ == '__main__':
    app.run()
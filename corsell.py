from app import app, db
from app.models import User, Product, Image

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'Image': Image}

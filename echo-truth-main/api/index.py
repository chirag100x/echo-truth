import sys
import os

# Add backend directory to sys.path so 'app' module can be found
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.main import app

from setuptools import setup

setup(
    name="mcts",
    version="0.1.0",
    install_requires=[
        "numpy>=1.21.0",  # Other dependencies
        "gym-connect4 @ git+https://github.com/Danielhp95/gym-connect4.git"
    ],
)

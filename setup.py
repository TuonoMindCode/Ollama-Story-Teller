from setuptools import setup, find_packages

setup(
    name="ollama-story-generator",
    version="1.0.4",
    description="AI Story Generator with Ollama Integration",
    packages=find_packages(),  # This will find ALL your packages/folders
    py_modules=[
        'main', 
        'app'
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "urllib3>=1.26.0",
        "colorama>=0.4.6",
        "python-dateutil>=2.8.2"
    ],
    include_package_data=True,
    package_data={
        '': ['*.py', '*.txt', '*.md'],
    },
)
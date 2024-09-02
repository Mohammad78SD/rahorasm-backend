from setuptools import setup, find_packages

setup(
    name="melipayamak",               # Name of your package
    version="0.1",                    # Version of your package
    packages=find_packages(),         # Automatically find the package directories
    include_package_data=True,        # Include other files specified in MANIFEST.in
    description="A Python package for sending SMS using Melipayamak API",
    author="Your Name",               # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    url="https://your-url.com",       # URL to the package's homepage (optional)
    install_requires=[                # List of dependencies
        # Add any dependencies here
    ],
)

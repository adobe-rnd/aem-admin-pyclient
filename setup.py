from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aem-admin-client",
    version="12.74.3",
    author="Satya Deep Maheshwari",
    author_email="satyam@adobe.com",
    description="A comprehensive Python client library for the AEM Admin API",
    long_description="A comprehensive Python client library for the AEM Admin API. "
    "This client is used to manage the lifecycle of content and code.",
    long_description_content_type="text/markdown",
    url="https://github.com/adobe-rnd/aem-admin-pyclient",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    license="Apache-2.0",
    keywords="aem admin api client adobe experience manager helix",
    project_urls={
        "Bug Reports": "https://github.com/adobe-rnd/aem-admin-pyclient/issues",
        "Source": "https://github.com/adobe-rnd/aem-admin-pyclient",
        "Documentation": "https://github.com/adobe-rnd/aem-admin-pyclient/blob/main/README.md",
    },
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantum-llvm-compiler",
    version="1.0.0",
    author="Quantum-LLVM Compiler Team",
    author_email="dev@quantum-llvm-compiler.org",
    description="A hybrid quantum-classical compiler supporting QASM and NASM to LLVM IR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityadhara040505/quantum-llvm-compiler",
    project_urls={
        "Bug Tracker": "https://github.com/adityadhara040505/quantum-llvm-compiler/issues",
        "Documentation": "https://github.com/adityadhara040505/quantum-llvm-compiler/docs",
        "Source Code": "https://github.com/adityadhara040505/quantum-llvm-compiler",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Assembly",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Compilers",
        "Topic :: System :: Hardware",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantum-llvm-compiler=main:main",
            "qlc=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml"],
        "examples": ["**/*"],
        "docs": ["**/*"],
    },
    zip_safe=False,
)
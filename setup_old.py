from setuptools import setup, find_packages

setup(
    name="quantum_llvm_compiler",
    version="0.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "llvmlite==0.43.0",
        "qiskit==1.11.0",
        "antlr4-python3-runtime==4.13",
        "numpy==1.26.0",
        "networkx==3.1",
        "sympy==1.12",
    ],
)

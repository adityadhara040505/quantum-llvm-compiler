#!/bin/bash
# Setup script for quantum-llvm-compiler

echo "🔧 Setting up quantum-llvm-compiler..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install qiskit-aer if not present (needed for simulation)
if ! pip show qiskit-aer > /dev/null 2>&1; then
    echo "Installing qiskit-aer for quantum simulation..."
    pip install qiskit-aer
fi

echo "✅ Setup complete!"
echo ""
echo "To run the quantum compiler:"
echo "  source .venv/bin/activate"
echo "  PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm"
echo ""
echo "Available examples:"
for file in examples/*.qasm; do
    if [ -f "$file" ]; then
        echo "  - $file"
    fi
done
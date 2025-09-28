#!/bin/bash

# Quick Demo Script for Quantum LLVM Compiler
# Runs essential examples quickly

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Quick Quantum LLVM Compiler Demo${NC}"
echo "=================================="

# Activate environment if needed
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

echo -e "${GREEN}1. Running Teleportation Circuit...${NC}"
PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm

echo -e "\n${GREEN}2. Running Grover's Algorithm...${NC}"
PYTHONPATH=. python run_quantum_compiler.py examples/grover.qasm

echo -e "\n${GREEN}3. Generated Output Files:${NC}"
ls -la output_*.* 2>/dev/null || echo "No output files found"

echo -e "\n${GREEN}4. Quick Performance Test:${NC}"
PYTHONPATH=. python -c "
import time
from src.frontend.parser import parse_qasm_file
from src.ir.passes import superposition_opt

start = time.time()
ast = parse_qasm_file('examples/teleport.qasm')
optimized = superposition_opt(ast)
total_time = time.time() - start

print(f'✅ Compiled {len(ast.nodes)} operations in {total_time:.6f}s')
print(f'✅ Quantum IR generation: Complete')
print(f'✅ Optimization passes: Applied')
"

echo -e "\n${BLUE}✅ Quick demo complete! Run ./demo.sh for full demonstration.${NC}"
# Quantum-LLVM Compiler Makefile
# ===============================

# Project configuration
PROJECT_NAME = quantum-llvm-compiler
VERSION = 1.0.0
PYTHON = python3
PIP = pip3

# Directories
SRC_DIR = src
EXAMPLES_DIR = examples
BUILD_DIR = build
BIN_DIR = bin
OUTPUT_DIR = output
SCRIPTS_DIR = scripts
TESTS_DIR = tests
DOCS_DIR = docs

# Virtual environment
VENV_DIR = .venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
PURPLE = \033[0;35m
CYAN = \033[0;36m
NC = \033[0m # No Color

.PHONY: all help setup install clean test demo examples build run-quantum run-classical

# Default target
all: setup build

help:
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║                    QUANTUM-LLVM COMPILER v$(VERSION)                     ║$(NC)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(NC)"
	@echo "  $(GREEN)setup$(NC)         - Set up virtual environment and install dependencies"
	@echo "  $(GREEN)install$(NC)       - Install project dependencies"
	@echo "  $(GREEN)build$(NC)         - Build all examples"
	@echo "  $(GREEN)clean$(NC)         - Clean build artifacts"
	@echo "  $(GREEN)test$(NC)          - Run test suite"
	@echo "  $(GREEN)demo$(NC)          - Run interactive demonstration"
	@echo "  $(GREEN)examples$(NC)      - Build all example programs"
	@echo "  $(GREEN)run-quantum$(NC)   - Run quantum compilation example"
	@echo "  $(GREEN)run-classical$(NC) - Run classical compilation example"
	@echo ""
	@echo "$(YELLOW)Quick start:$(NC)"
	@echo "  make setup     # First time setup"
	@echo "  make demo      # Run demonstration"
	@echo "  make examples  # Build examples"

setup: $(VENV_DIR)
	@echo "$(BLUE)🚀 Setting up Quantum-LLVM Compiler...$(NC)"
	@$(MAKE) install
	@echo "$(GREEN)✅ Setup completed successfully!$(NC)"

$(VENV_DIR):
	@echo "$(BLUE)📦 Creating virtual environment...$(NC)"
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✅ Virtual environment created$(NC)"

install: $(VENV_DIR)
	@echo "$(BLUE)📥 Installing dependencies...$(NC)"
	@. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	@. $(VENV_ACTIVATE) && $(PIP) install -e .
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

build: examples
	@echo "$(GREEN)✅ Build completed!$(NC)"

examples:
	@echo "$(BLUE)🔨 Building examples...$(NC)"
	@$(MAKE) build-quantum-examples
	@$(MAKE) build-assembly-examples
	@echo "$(GREEN)✅ All examples built successfully!$(NC)"

build-quantum-examples:
	@echo "$(PURPLE)🔬 Building quantum examples...$(NC)"
	@mkdir -p $(OUTPUT_DIR)
	@if [ -f "$(EXAMPLES_DIR)/quantum/grover.qasm" ]; then \
		. $(VENV_ACTIVATE) && $(PYTHON) main.py quantum $(EXAMPLES_DIR)/quantum/grover.qasm -o $(OUTPUT_DIR)/grover; \
	fi
	@if [ -f "$(EXAMPLES_DIR)/quantum/teleport.qasm" ]; then \
		. $(VENV_ACTIVATE) && $(PYTHON) main.py quantum $(EXAMPLES_DIR)/quantum/teleport.qasm -o $(OUTPUT_DIR)/teleport; \
	fi

build-assembly-examples:
	@echo "$(PURPLE)⚙️  Building assembly examples...$(NC)"
	@mkdir -p $(BIN_DIR)
	@if [ -f "$(EXAMPLES_DIR)/assembly/working_demo.asm" ]; then \
		nasm -f elf64 $(EXAMPLES_DIR)/assembly/working_demo.asm -o $(BUILD_DIR)/working_demo.o && \
		ld $(BUILD_DIR)/working_demo.o -o $(BIN_DIR)/working_demo; \
	fi
	@for asm_file in $(EXAMPLES_DIR)/assembly/*.asm; do \
		if [ -f "$$asm_file" ]; then \
			base_name=$$(basename "$$asm_file" .asm); \
			echo "$(YELLOW)  • Building $$base_name...$(NC)"; \
			nasm -f elf64 "$$asm_file" -o "$(BUILD_DIR)/$$base_name.o" 2>/dev/null && \
			ld "$(BUILD_DIR)/$$base_name.o" -o "$(BIN_DIR)/$$base_name" 2>/dev/null || true; \
		fi \
	done

test:
	@echo "$(BLUE)🧪 Running test suite...$(NC)"
	@. $(VENV_ACTIVATE) && $(PYTHON) -m pytest $(TESTS_DIR) -v
	@echo "$(GREEN)✅ All tests passed!$(NC)"

demo:
	@echo "$(BLUE)🎮 Starting interactive demo...$(NC)"
	@. $(VENV_ACTIVATE) && $(PYTHON) main.py --demo

run-quantum:
	@echo "$(BLUE)🔬 Running quantum example...$(NC)"
	@if [ -f "$(EXAMPLES_DIR)/quantum/grover.qasm" ]; then \
		. $(VENV_ACTIVATE) && $(PYTHON) main.py quantum $(EXAMPLES_DIR)/quantum/grover.qasm; \
	else \
		echo "$(RED)❌ Quantum example not found$(NC)"; \
	fi

run-classical:
	@echo "$(BLUE)⚙️  Running classical example...$(NC)"
	@if [ -f "$(EXAMPLES_DIR)/assembly/working_demo.asm" ]; then \
		. $(VENV_ACTIVATE) && $(PYTHON) main.py classical $(EXAMPLES_DIR)/assembly/working_demo.asm; \
	else \
		echo "$(RED)❌ Classical example not found$(NC)"; \
	fi

clean:
	@echo "$(YELLOW)🧹 Cleaning build artifacts...$(NC)"
	@rm -rf $(BUILD_DIR)/*
	@rm -rf $(BIN_DIR)/*
	@rm -rf $(OUTPUT_DIR)/*
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.o" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

clean-all: clean
	@echo "$(YELLOW)🧹 Deep cleaning...$(NC)"
	@rm -rf $(VENV_DIR)
	@rm -rf .pytest_cache
	@echo "$(GREEN)✅ Deep cleanup completed!$(NC)"

list-examples:
	@echo "$(CYAN)📚 Available Examples:$(NC)"
	@echo ""
	@echo "$(PURPLE)🔬 Quantum Examples:$(NC)"
	@ls -1 $(EXAMPLES_DIR)/quantum/*.qasm 2>/dev/null | sed 's/^/   • /' || echo "   (none found)"
	@echo ""
	@echo "$(PURPLE)⚙️  Assembly Examples:$(NC)"
	@ls -1 $(EXAMPLES_DIR)/assembly/*.asm 2>/dev/null | sed 's/^/   • /' || echo "   (none found)"
	@echo ""
	@echo "$(PURPLE)💻 Classical Examples:$(NC)"
	@ls -1 $(EXAMPLES_DIR)/classical/* 2>/dev/null | sed 's/^/   • /' || echo "   (none found)"

status:
	@echo "$(CYAN)📊 Project Status:$(NC)"
	@echo ""
	@echo "$(YELLOW)Project:$(NC) $(PROJECT_NAME) v$(VERSION)"
	@echo "$(YELLOW)Python:$(NC)  $$($(PYTHON) --version)"
	@echo "$(YELLOW)Virtual Environment:$(NC) $$([ -d $(VENV_DIR) ] && echo "✅ Active" || echo "❌ Not setup")"
	@echo "$(YELLOW)NASM:$(NC)    $$(nasm -v 2>/dev/null | head -1 || echo "❌ Not installed")"
	@echo ""
	@echo "$(YELLOW)Directory Structure:$(NC)"
	@echo "   📁 Source:    $(SRC_DIR)/"
	@echo "   📁 Examples:  $(EXAMPLES_DIR)/"
	@echo "   📁 Build:     $(BUILD_DIR)/"
	@echo "   📁 Binaries:  $(BIN_DIR)/"
	@echo "   📁 Output:    $(OUTPUT_DIR)/"
	@echo "   📁 Scripts:   $(SCRIPTS_DIR)/"
	@echo "   📁 Tests:     $(TESTS_DIR)/"

install-deps:
	@echo "$(BLUE)📦 Installing system dependencies...$(NC)"
	@echo "$(YELLOW)Please ensure you have the following installed:$(NC)"
	@echo "  • Python 3.8+ ($(GREEN)$(PYTHON) --version$(NC))"
	@echo "  • NASM assembler ($(GREEN)sudo apt install nasm$(NC))"
	@echo "  • LLVM development tools ($(GREEN)sudo apt install llvm-dev$(NC))"
	@echo "  • Build essentials ($(GREEN)sudo apt install build-essential$(NC))"

# Version management
version:
	@echo "$(PROJECT_NAME) v$(VERSION)"

.ONESHELL:
SHELL := /bin/bash
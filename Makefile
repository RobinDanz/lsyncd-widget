PYTHON := python3
REQUIREMENTS := requirements.txt

.PHONY: test all setup setup-system setup-python setup-macos setup-pi run clean help

all: setup

setup: setup-system setup-python

setup-system:  ## Installe les paquets système selon la plateforme
ifeq ($(shell uname),Darwin)
	@echo "OS: macOS. Installing required packages"
	$(PYTHON) -m pip install $(REQUIREMENTS)
else ifeq ($(shell uname),Linux)
	@echo "OS: Linux. Installing required packages."
	sudo apt update -qq
	sudo apt install -y python3-PyQt6 python3-watchdog
else
	$(error Système non supporté)
endif

setup-python:  ## Installe les dépendances Python communes
	@echo "Installation des dépendances Python..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

run:  ## Lance l'application
	@echo "Lancement de LogTracker..."
	$(PYTHON) main.py

clean:
	@echo "Nettoyage..."
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:  ## Affiche la liste des commandes disponibles
	@echo "Commandes disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(:|##)"}; {printf "  \033[35m%-20s\033[0m %s\n", $$1, $$3}'
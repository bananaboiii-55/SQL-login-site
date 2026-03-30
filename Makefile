.PHONY: help install run-vulnerable run-secure run-both clean

help:
	@echo "SQL Injection Practice Lab"
	@echo ""
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make run-vulnerable  - Run vulnerable app on port 5000"
	@echo "  make run-secure      - Run secure app on port 5001"
	@echo "  make run-both        - Run both apps (vulnerable on 5000, secure on 5001)"
	@echo "  make clean           - Remove database files"

install:
	pip install -r requirements.txt

run-vulnerable:
	python app_vulnerable.py

run-secure:
	python app_secure.py

run-both:
	@echo "Starting vulnerable app on port 5000..."
	python app_vulnerable.py &
	@echo "Starting secure app on port 5001..."
	python app_secure.py &
	@echo "Both apps are running!"
	@echo "Vulnerable: http://localhost:5000"
	@echo "Secure: http://localhost:5001"
	@echo "Press Ctrl+C to stop"
	@wait

clean:
	rm -f users.db users_secure.db
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

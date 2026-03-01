.PHONY: render preview screenshot clean install lint help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

render: ## Render the full intro video to output/intro.mp4
	python src/main.py

preview: ## Render with live Pygame preview window
	python src/main.py --preview

screenshot: output/intro.mp4 ## Extract a screenshot from the rendered video
	ffmpeg -y -i output/intro.mp4 -vf "select=eq(n\,60)" -frames:v 1 -update 1 assets/screenshot.png

clean: ## Remove rendered output (frames, audio, video)
	rm -rf output/frames output/audio.wav output/intro.mp4

install: ## Install Python dependencies into active venv
	pip install -r requirements.txt

lint: ## Run ruff linter on source
	ruff check src/

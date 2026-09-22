@_default:
  just --list

@lint:
  echo mypy
  just --justfile {{justfile()}} mypy
  echo ruff-format
  just --justfile {{justfile()}} ruff-format
  echo ruff-check
  just --justfile {{justfile()}} ruff-check

@mypy:
  uv run mypy cfgts tests

@ruff-check:
  uv run ruff check cfgts tests

@ruff-format:
  uv run ruff format cfgts tests

@test *args="":
  -uv run pytest {{args}}

@lock:
  uv lock

@lock-upgrade:
  uv lock --upgrade

@install:
  uv sync --frozen --all-extras

@latex-pdf:
  pdflatex -file-line-error -output-directory=docs/report docs/report/report.tex

@clean-latex:
  rm ./docs/report/pdfa.xmpi || true
  rm ./docs/report/report.aux || true
  rm ./docs/report/report.bcf || true
  rm ./docs/report/report.lof || true
  rm ./docs/report/report.log || true
  rm ./docs/report/report.lot || true
  rm ./docs/report/report.bbl || true
  rm ./docs/report/report.blg || true
  rm ./docs/report/report.out || true
  rm ./docs/report/report.run.xml || true
  rm ./docs/report/report.toc || true

@clean:
    rm -rf .venv || true
    rm -rf .pytest_cache || true
    rm -rf .mypy_cache || true
    rm -rf **/.mypy_cache || true
    rm -rf **/**/.mypy_cache || true
    rm -rf .ruff_cache || true
    rm -rf .uv || true
    rm -rf __pycache__ || true
    rm -rf **/__pycache__ || true
    rm -rf **/**/__pycache__ || true

@docs:
  just install
  just clean-latex
  # Two times to render the bibliography
  just latex-pdf
  biber ./docs/report/report
  just latex-pdf
  cp ppt/output.html docs/presentation.html
  uv run mkdocs build

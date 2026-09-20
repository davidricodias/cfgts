#!/usr/bin/env bash
# Renders every scene in ppt/scenes/ (one script per slide) and packages
# them into a single self-contained HTML file (video assets embedded as
# data URIs). Fully self-contained: uses `uv run --no-project` to fetch
# manim/manim-slides into an ephemeral environment, independent of the root
# cfgts venv and of presentation/'s.
set -euo pipefail
cd "$(dirname "$0")"

QUALITY="${1:-h}"   # l=480p15 (draft), m=720p30, h=1080p60
case "$QUALITY" in
  l) ;;
  m) ;;
  h) ;;
  *) echo "Uso: $0 [l|m|h]"; exit 1 ;;
esac
# NOTE: must pass "--quality h" as two argv tokens, NOT "-qh": manim-slides'
# click parser splits unknown short-option clusters char by char, and since
# its own help flag is registered as exactly "-h", "-qh" gets misdetected as
# "-h" and just prints the help text instead of rendering (silently, exit 0).

# One (file, scene) pair per slide, in presentation order. s05-s14 are
# empty chapter-divider placeholders for report.tex chapters not yet
# scripted (content pending). Filenames are numbered to match this order.
SCENES=(
  "s00_title.py:TitleSlide"
  "s01_intro.py:IntroSlide"
  "s02_phases.py:PhasesSlide"
  "s03_motivation_finance.py:MotivationFinanceSlide"
  "s05_fundamentos.py:FundamentosSlide"
  "s06_estado_arte.py:EstadoArteSlide"
  "s07_analisis_problema.py:AnalisisProblemaSlide"
  "s08_resultados.py:ResultadosSlide"
  "s09_marco_regulador.py:MarcoReguladorSlide"
  "s10_impacto.py:ImpactoSlide"
  "s11_planificacion.py:PlanificacionSlide"
  "s12_presupuesto.py:PresupuestoSlide"
  "s13_conclusiones.py:ConclusionesSlide"
  "s14_futuras_lineas.py:FuturasLineasSlide"
  "s15_closing.py:ClosingSlide"
)

UV_RUN=(uv run --no-project --with "manim>=0.18.1" --with "manim-slides>=5.7.0" --with numpy)

rm -rf scenes/slides scenes/media

cd scenes
for entry in "${SCENES[@]}"; do
  file="${entry%%:*}"
  scene="${entry##*:}"
  echo ">>> Renderizando $scene ($file)"
  "${UV_RUN[@]}" manim-slides render --quality "$QUALITY" "$file" "$scene"
done
cd ..

SCENE_NAMES=()
for entry in "${SCENES[@]}"; do
  SCENE_NAMES+=("${entry##*:}")
done

echo ">>> Empaquetando en un único HTML"
(cd scenes && "${UV_RUN[@]}" manim-slides convert "${SCENE_NAMES[@]}" ../output.html --one-file \
  --use-template ../template.html)

echo ">>> Listo: $(pwd)/output.html"

#!/usr/bin/env bash
# Renders every scene in ppt/scenes/ (one script per slide) and packages
# them into a single self-contained HTML file (video assets embedded as
# data URIs). Fully self-contained: uses `uv run --no-project` to fetch
# manim/manim-slides into an ephemeral environment, independent of the root
# cfgts venv and of presentation/'s.
# Usage: ./generate.sh [l|m|h] [--clean]  (see CLEAN comment below for --clean)
set -euo pipefail
cd "$(dirname "$0")"

QUALITY="h"   # l=480p15 (draft), m=720p30, h=1080p60
CLEAN=0
for arg in "$@"; do
  case "$arg" in
    l|m|h) QUALITY="$arg" ;;
    --clean) CLEAN=1 ;;
    *) echo "Uso: $0 [l|m|h] [--clean]"; exit 1 ;;
  esac
done
# NOTE: must pass "--quality h" as two argv tokens, NOT "-qh": manim-slides'
# click parser splits unknown short-option clusters char by char, and since
# its own help flag is registered as exactly "-h", "-qh" gets misdetected as
# "-h" and just prints the help text instead of rendering (silently, exit 0).

# One (file, scene) pair per slide, in presentation order: roughly one scene
# per report.tex chapter, with the "Propuesta" chapter split across s06-s11
# (one slide per phase, a summary, the implementation and a usage example).
# Filenames are numbered to match this order.
SCENES=(
  "s00_title.py:TitleSlide"
  "s01_intro.py:IntroSlide"
  "s02_motivation_finance.py:MotivationFinanceSlide"
  "s03_fundamentos.py:FundamentosSlide"
  "s04_estado_arte.py:EstadoArteSlide"
  "s05_analisis_problema.py:AnalisisProblemaSlide"
  "s06_propuesta_fase1.py:PropuestaFase1Slide"
  "s07_propuesta_fase2.py:PropuestaFase2Slide"
  "s08_propuesta_fase3.py:PropuestaFase3Slide"
  "s09_propuesta_resumen.py:PropuestaResumenSlide"
  "s10_implementacion.py:ImplementacionSlide"
  "s11_ejemplo_uso.py:EjemploUsoSlide"
  "s12_resultados.py:ResultadosSlide"
  "s13_marco_regulador.py:MarcoReguladorSlide"
  "s14_impacto.py:ImpactoSlide"
  "s15_planificacion.py:PlanificacionSlide"
  "s16_presupuesto.py:PresupuestoSlide"
  "s17_futuras_lineas.py:FuturasLineasSlide"
  "s18_conclusiones.py:ConclusionesSlide"
  "s19_closing.py:ClosingSlide"
)

UV_RUN=(uv run --no-project --with "manim==0.21.0" --with "manim-slides==5.7.0" --with "numpy==2.5.3")

# scenes/media/videos/*/*/partial_movie_files/ is Manim's own render cache
# (keyed by a hash of each animation's content): keeping it across runs lets
# unchanged slides be skipped ("Animation already saved") instead of fully
# re-rendered, which is what makes incremental `generate.sh` calls fast. Only
# wipe it with `--clean` (e.g. after renaming/removing a scene, or if a
# stale-cache render looks wrong).
if [[ "$CLEAN" == "1" ]]; then
  echo ">>> Limpiando caché (--clean)"
  rm -rf scenes/slides scenes/media
fi

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

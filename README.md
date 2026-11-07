# Does AI use follow the job mix?

Is cross-country variation in AI use explained by differences in occupational structure? This project relates usage from the Anthropic Economic Index to the European occupational mix (Eurostat LFS) through occupation-level AI exposure measures and SOC/ISCO crosswalks.

## Data sources

| Source | Dataset | Location | Access |
|---|---|---|---|
| Anthropic Economic Index | `aei_claude_ai_2026-06-26.csv`, `data_documentation.md` (release 2026-06-26) | `data/raw/anthropic` | [Hugging Face](https://huggingface.co/datasets/Anthropic/EconomicIndex) |
| Eurostat | `lfsa_egai2d`: employment by sex, age and occupation (ISCO-08, 2-digit) | `data/raw/eurostat` | [Eurostat API](https://ec.europa.eu/eurostat/databrowser/view/lfsa_egai2d/default/table) |
| Eurostat | `nama_10_pc`: main GDP aggregates per capita | `data/raw/eurostat` | [Eurostat API](https://ec.europa.eu/eurostat/databrowser/view/nama_10_pc/default/table) |
| Eloundou et al. (2024), *GPTs are GPTs* | `occ_level.csv`: occupation-level exposure | `data/raw/exposure` | [GitHub](https://github.com/openai/GPTs-are-GPTs) |
| BLS | SOC 2010 to 2018 crosswalk | `data/raw/bls` | [manual](https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx) |
| BLS | ISCO-08 to SOC crosswalk | `data/raw/bls` | [manual](https://www.bls.gov/soc/ISCO_SOC_Crosswalk.xls) |
| BLS | OEWS national estimates, May 2025 | `data/raw/bls` | [manual](https://www.bls.gov/oes/special-requests/oesm25nat.zip) |

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/download.py
```

BLS rejects scripted downloads. Save the three BLS files to `data/raw/bls` by hand from a browser.

## Layout

```
data/raw/        source files (not tracked)
data/processed/  derived data (not tracked)
notebooks/
src/
output/figures/
output/tables/
paper/
```

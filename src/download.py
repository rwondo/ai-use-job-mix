"""Download raw data into data/raw. Existing files are skipped."""

import gzip
import shutil
import tempfile
import urllib.request
from pathlib import Path

from huggingface_hub import hf_hub_download

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

HF_REPO = "Anthropic/EconomicIndex"
HF_RELEASE = "release_2026_06_26"
HF_FILES = [
    f"{HF_RELEASE}/data/aei_claude_ai_2026-06-26.csv",
    f"{HF_RELEASE}/data_documentation.md",
]

EUROSTAT_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
    "{code}?format=TSV&compressed=true"
)
EUROSTAT_CODES = ["lfsa_egai2d", "nama_10_pc"]

EXPOSURE_URL = (
    "https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/occ_level.csv"
)

BLS_URLS = [
    "https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx",
    "https://www.bls.gov/soc/ISCO_SOC_Crosswalk.xls",
    "https://www.bls.gov/oes/special-requests/oesm25nat.zip",
]


def exists(dest: Path) -> bool:
    if dest.exists():
        print(f"skip  {dest.relative_to(RAW)}")
        return True
    return False


def fetch(url: str, dest: Path, gunzip: bool = False) -> None:
    if exists(dest):
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib"})
    with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(gzip.GzipFile(fileobj=r) if gunzip else r, f)
    tmp.replace(dest)
    print(f"saved {dest.relative_to(RAW)}")


def anthropic() -> None:
    out = RAW / "anthropic"
    for name in HF_FILES:
        dest = out / Path(name).name
        if exists(dest):
            continue
        with tempfile.TemporaryDirectory(dir=out) as tmp:
            path = hf_hub_download(HF_REPO, name, repo_type="dataset", local_dir=tmp)
            shutil.move(path, dest)
        print(f"saved {dest.relative_to(RAW)}")


def eurostat() -> None:
    for code in EUROSTAT_CODES:
        fetch(EUROSTAT_URL.format(code=code), RAW / "eurostat" / f"{code}.tsv", gunzip=True)


def exposure() -> None:
    fetch(EXPOSURE_URL, RAW / "exposure" / "occ_level.csv")


def bls() -> None:
    out = RAW / "bls"
    missing = [u for u in BLS_URLS if not (out / u.rsplit("/", 1)[1]).exists()]
    if not missing:
        print("skip  bls files")
        return
    print(f"\nBLS blocks scripted downloads. Save these manually into {out}:")
    for u in missing:
        print(f"  {u}")


def main() -> None:
    for d in ("anthropic", "eurostat", "exposure", "bls"):
        (RAW / d).mkdir(parents=True, exist_ok=True)
    anthropic()
    eurostat()
    exposure()
    bls()


if __name__ == "__main__":
    main()

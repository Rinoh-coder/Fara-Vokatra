#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   DRIVE_PARENT_ID=<folder-id> scripts/archive_year_to_drive.sh 1991 /tmp/fara-vokatra-1991
# Le dossier parent doit être créé ou choisi explicitement par l’utilisateur.
YEAR="${1:?année requise}"
DATA_ROOT="${2:?racine locale requise}"
PARENT_ID="${DRIVE_PARENT_ID:?définir DRIVE_PARENT_ID explicitement}"
MANIFEST="${DATA_ROOT}/processed/chirps/manifests/year_${YEAR}_rnl_final.json"
REPORT="${DATA_ROOT}/processed/chirps/manifests/year_${YEAR}_quality.json"

[[ -s "${MANIFEST}" ]] || { echo "Manifeste absent: ${MANIFEST}" >&2; exit 1; }
python3 - "${MANIFEST}" "${REPORT}" <<'PY'
import json, sys
from pathlib import Path
manifest = json.loads(Path(sys.argv[1]).read_text())
if not manifest.get('records'):
    raise SystemExit('Manifeste vide')
PY
python3 -m src.annual_quality --manifest "${MANIFEST}" --output "${REPORT}"
python3 - "${REPORT}" <<'PY'
import json, sys
from pathlib import Path
report = json.loads(Path(sys.argv[1]).read_text())
if report.get('valid') is not True:
    raise SystemExit('Archivage refusé: rapport qualité invalide')
PY

create_folder() {
  local name="$1" parent="$2"
  local query
  query=$(printf "name = '%s' and '%s' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false" "$name" "$parent")
  local found
  found=$(gws drive files list --params "$(python3 -c 'import json,sys; print(json.dumps({"q":sys.argv[1],"pageSize":10,"fields":"files(id,name)"}))' "$query")" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("files",[{}])[0].get("id",""))')
  if [[ -n "$found" ]]; then echo "$found"; return; fi
  gws drive files create --json "$(python3 -c 'import json,sys; print(json.dumps({"name":sys.argv[1],"mimeType":"application/vnd.google-apps.folder","parents":[sys.argv[2]]}))' "$name" "$parent")" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])'
}

YEAR_ID=$(create_folder "${YEAR}" "${PARENT_ID}")
for zone in northwest east highlands west south; do
  ZONE_ID=$(create_folder "${zone}" "${YEAR_ID}")
  shopt -s nullglob
  files=("${DATA_ROOT}/processed/chirps/final/rnl/${zone}"/*.tif)
  shopt -u nullglob
  for file in "${files[@]}"; do
    gws drive files create --upload "$file" --upload-content-type image/tiff --json "$(python3 -c 'import json,sys; print(json.dumps({"name":sys.argv[1],"parents":[sys.argv[2]]}))' "$(basename "$file")" "$ZONE_ID")" >/dev/null
  done
done
for file in "${MANIFEST}" "${REPORT}"; do
  gws drive files create --upload "$file" --upload-content-type application/json --json "$(python3 -c 'import json,sys; print(json.dumps({"name":sys.argv[1],"parents":[sys.argv[2]]}))' "$(basename "$file")" "$YEAR_ID")" >/dev/null
done
printf 'Archive Drive créée pour %s dans %s\n' "$YEAR" "$YEAR_ID"

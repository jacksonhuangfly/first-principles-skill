#!/bin/bash
# Download SRT/VTT subtitles in the selected language: manual, then automatic.
# Usage: ./download_subtitles.sh [--language en|zh-CN] <YouTube_URL> [output_directory]
# Requires yt-dlp; no subtitle conversion or ffmpeg is needed.
set -euo pipefail

usage() {
    echo "Usage: $0 [--language en|zh-CN] <YouTube_URL> [output_directory]"
    echo "Default language: en. Options may appear before or after the URL/output directory."
    echo "Try manual subtitles, then automatic subtitles in the selected language only."
    echo "en selects en and its variants; zh-CN selects zh-Hans/zh-CN and their variants."
}

SUBTITLE_LANGUAGE="en"
POSITIONALS=()
while (( $# )); do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --language)
            if (( $# < 2 )) || [[ -z "$2" || "$2" == -* ]]; then
                echo "Error: --language requires en or zh-CN." >&2
                exit 2
            fi
            SUBTITLE_LANGUAGE="$2"
            shift 2
            ;;
        --language=*) SUBTITLE_LANGUAGE="${1#*=}"; shift ;;
        --) shift; POSITIONALS+=("$@"); break ;;
        -*) echo "Error: unknown option: $1" >&2; usage >&2; exit 2 ;;
        *) POSITIONALS+=("$1"); shift ;;
    esac
done

case "$SUBTITLE_LANGUAGE" in
    en) SUBTITLE_TRACKS="en(?:-.*)?" ;;
    zh-CN) SUBTITLE_TRACKS="zh-Hans(?:-.*)?,zh-CN(?:-.*)?" ;;
    *) echo "Error: unsupported language '$SUBTITLE_LANGUAGE'; choose en or zh-CN." >&2; exit 2 ;;
esac
if (( ${#POSITIONALS[@]} < 1 || ${#POSITIONALS[@]} > 2 )); then
    usage >&2
    exit 2
fi
URL="${POSITIONALS[0]}"
OUTPUT_DIR="${POSITIONALS[1]:-.}"
if [[ -z "$URL" || -z "$OUTPUT_DIR" ]]; then
    echo "Error: URL and output directory must not be empty." >&2
    exit 2
fi
if ! command -v yt-dlp >/dev/null 2>&1; then
    echo "Error: install yt-dlp before downloading subtitles." >&2
    exit 1
fi
mkdir -p "$OUTPUT_DIR"
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT
shopt -s nullglob

download() {
    local kind="$1" languages="$2" attempt="$3"
    local attempt_dir="$WORK_DIR/$attempt"
    mkdir -p "$attempt_dir"
    echo ">>> Trying $attempt subtitles..."
    if yt-dlp --ignore-config "$kind" --sub-langs "$languages" --sub-format "srt/vtt" \
        --skip-download --no-playlist -o "$attempt_dir/%(id)s.%(ext)s" "$URL"; then
        # Every attempt has a new directory, so unrelated old files cannot pass.
        local files=("$attempt_dir"/*.srt "$attempt_dir"/*.vtt)
        if (( ${#files[@]} )); then
            if ! cp "${files[@]}" "$OUTPUT_DIR/"; then
                echo "Error: could not save downloaded subtitles to $OUTPUT_DIR" >&2
                return 1
            fi
            local file
            for file in "${files[@]}"; do
                echo "Downloaded: $OUTPUT_DIR/${file##*/}"
            done
            return 0
        fi
    fi
    return 1
}

if download --write-subs "$SUBTITLE_TRACKS" "manual-$SUBTITLE_LANGUAGE"; then exit 0; fi
if download --write-auto-subs "$SUBTITLE_TRACKS" "automatic-$SUBTITLE_LANGUAGE"; then exit 0; fi
echo "No SRT/VTT subtitles downloaded for selected language: $SUBTITLE_LANGUAGE." >&2
exit 1

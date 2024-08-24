#!/usr/bin/env bash
set -ex

# Define variables
REMOTEDIR="/data/lexbor.com/docs/www/"
TODAY=$(date '+%F')
TMPDIR="/tmp/$TODAY"
BACKUPDIR="backup/$TODAY.tar.gz"

# Clean up the working directory
make clean-doc

# Remove unnecessary files from the source directory
find source/ -type f \( -name '*.orig' -o -name '*.rej' -o -name '* 2.*' -o -name '*.pyc' -o -name '.DS_Store' \) -delete

# Backup the remote directory
rsync -rctv "lexbor.com:${REMOTEDIR}" "$TMPDIR/"
tar -zcvf "$BACKUPDIR" "$TMPDIR" && rm -rf "$TMPDIR"

# Sync remote directory to local deploy directory
rsync -rctv "lexbor.com:${REMOTEDIR}" deploy/

# Deploy the project
make deploy

# Dry-run: Sync deploy directory back to the remote directory to verify changes
rsync -rctvn deploy/ "lexbor.com:${REMOTEDIR}"

# If dry-run looks good, sync deploy directory to remote directory
rsync -rctv deploy/ "lexbor.com:${REMOTEDIR}"

# Clean up after deployment
make clean-doc

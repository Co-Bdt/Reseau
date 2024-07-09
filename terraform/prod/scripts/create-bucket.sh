#!/bin/bash
PROJECT_ID="reseau-devperso"

gsutil mb -p $PROJECT_ID -l us -b on "gs://tf-state-prod-reseau-devperso"
gsutil versioning set on "gs://tf-state-prod-reseau-devperso"

# rand="$(echo $RANDOM)"
# gsutil mb -p $PROJECT_ID -l us -b on "gs://tf-state-$rand"
# gsutil versioning set on "gs://tf-state-$rand"
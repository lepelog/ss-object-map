#!/usr/bin/env sh

# abort on errors
set -e

# build
NODE_OPTIONS="--openssl-legacy-provider --no-experimental-fetch" npm run build

# navigate into the build output directory
cd dist

git init -b master
git add -A
git commit -m 'deploy'

git push -f git@github.com:lepelog/ss-object-map.git master:gh-pages
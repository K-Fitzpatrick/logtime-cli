# Set version in setup and changelog, then commit

set -e
NEW_VERSION=$1

# Check: provided version number
if [ -z $NEW_VERSION ]; then
   echo 'ERROR: Provide a version number'
   exit 1
fi

# Check: untracked changes
GIT_STAGE=$(git status -s CHANGELOG.md setup.py)
if [ ! -z "$GIT_STAGE" ]; then
   echo 'ERROR: You have untracked changes; stash and try again.'
   exit 1
fi

# Check: version number bigger
OLD_VERSION=$(sed -rne "s/ *version='(.*)',/\1/p" setup.py)

if [ "$OLD_VERSION" = "$NEW_VERSION" ]; then
   echo "ERROR: Given version is the same as the old version"
   exit 1
fi

IFS='.' read -ra OLD_VERSION_PARTS <<< "$OLD_VERSION"
IFS='.' read -ra NEW_VERSION_PARTS <<< "$NEW_VERSION"
for i in 0 1 2; do
   if [ ${NEW_VERSION_PARTS[i]} -gt ${OLD_VERSION_PARTS[i]} ]; then
      break
   fi
   if [ ${NEW_VERSION_PARTS[i]} -lt ${OLD_VERSION_PARTS[i]} ]; then
      echo "ERROR: $NEW_VERSION is smaller than $OLD_VERSION"
      exit 1
   fi
done

# setup.py
sed "s/version='.*'/version='$NEW_VERSION'/" setup.py > temp
mv temp setup.py

# CHANGELOG.md
NOW=$(date +%Y-%m-%d)
sed "s/## Unreleased/## Unreleased\n\n## $NEW_VERSION - $NOW/" CHANGELOG.md > temp
mv temp CHANGELOG.md

# Commit changes
git add setup.py CHANGELOG.md
git commit -m "Update version to $NEW_VERSION"

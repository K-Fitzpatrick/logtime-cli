set -e
RELEASE_VERSION=$(sed -rne "s/ *version='(.*)',/\1/p" setup.py)

# Check: untracked changes
GIT_STAGE=$(git status -s)
if [ ! -z "$GIT_STAGE" ]; then
   echo 'ERROR: You have untracked changes; stash and try again.'
   exit 1
fi

# Check: already have tag
git fetch --tags
if [ $(git tag -l "v$RELEASE_VERSION") ]; then
   echo "ERROR: The tag 'v$RELEASE_VERSION' already exists"
   exit 1
fi

# Release to PyPi
python setup.py sdist upload

# Git tag
git tag "v$RELEASE_VERSION"
git push origin "v$RELEASE_VERSION"

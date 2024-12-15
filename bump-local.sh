#!/bin/bash

# Function to print usage
print_usage() {
    echo "Usage: $0 [frontend|backend|all]"
    echo "  frontend: bump only frontend version"
    echo "  backend: bump only backend version"
    echo "  all: bump both versions (default)"
    exit 1
}

# Function to bump version
bump_version() {
    local version_file=$1
    local current_version=$(cat $version_file)
    local major=$(echo $current_version | cut -d. -f1)
    local minor=$(echo $current_version | cut -d. -f2)
    local patch=$(echo $current_version | cut -d. -f3)
    local new_patch=$((patch + 1))
    local new_version="$major.$minor.$new_patch"
    echo $new_version > $version_file
    echo $new_version
}

# Parse command line arguments
COMPONENT=${1:-all}
case $COMPONENT in
    frontend|backend|all) ;;
    *) print_usage ;;
esac

# Bump and build based on component
if [ "$COMPONENT" = "frontend" ] || [ "$COMPONENT" = "all" ]; then
    # Bump frontend version
    FRONTEND_VERSION=$(bump_version frontend/version.txt)
    echo "Bumped frontend version to $FRONTEND_VERSION"

    # Build and push frontend
    echo "Building frontend image..."
    docker buildx build \
        --platform linux/arm64 \
        --build-arg VERSION=$FRONTEND_VERSION \
        -t ghcr.io/gurghet/social-engineering-game-frontend:$FRONTEND_VERSION \
        -t ghcr.io/gurghet/social-engineering-game-frontend:latest \
        --push \
        frontend/
fi

if [ "$COMPONENT" = "backend" ] || [ "$COMPONENT" = "all" ]; then
    # Bump backend version
    BACKEND_VERSION=$(bump_version server/version.txt)
    echo "Bumped backend version to $BACKEND_VERSION"

    # Build and push backend
    echo "Building backend image..."
    docker buildx build \
        --platform linux/arm64 \
        --build-arg VERSION=$BACKEND_VERSION \
        -t ghcr.io/gurghet/social-engineering-game-backend:$BACKEND_VERSION \
        -t ghcr.io/gurghet/social-engineering-game-backend:latest \
        --push \
        server/
fi

echo "Done! New versions:"
[ -n "$FRONTEND_VERSION" ] && echo "Frontend: $FRONTEND_VERSION"
[ -n "$BACKEND_VERSION" ] && echo "Backend: $BACKEND_VERSION"

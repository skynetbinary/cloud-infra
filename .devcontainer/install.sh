# Install asdf plugin manager.
asdf plugin add asdf-plugin-manager https://github.com/asdf-community/asdf-plugin-manager.git
asdf install asdf-plugin-manager latest
asdf global asdf-plugin-manager latest

# Add all plugins.
ASDF_PLUGIN_MANAGER_PLUGIN_VERSIONS_FILENAME=.devcontainer/.plugin-versions asdf-plugin-manager add-all

# Install asdf packages:
# poetry
asdf install poetry latest
asdf global poetry latest

# aws-vault
asdf install aws-vault latest
asdf global aws-vault latest

# pulumi
asdf install pulumi latest
asdf global pulumi latest

# Install project and dependencies with poetry.
poetry install

# direnv
find . -name .envrc -execdir direnv allow \;
asdf direnv setup --shell /usr/bin/bash --version latest

# Setup AWS config.
mkdir -p ~/.aws/
cp .devcontainer/files/aws-config ~/.aws/config

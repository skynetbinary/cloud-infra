FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm


ARG ASDF_BRANCH="v0.14.1"

# Install security updates and runtime dependencies if specified
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get install -y --no-install-recommends bash-completion && \
    apt-get clean && rm -r /var/lib/apt/lists


# We want to configure for the `vscode` user.
USER vscode

# Install asdf.
RUN git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch ${ASDF_BRANCH}
RUN echo "\n. $HOME/.asdf/asdf.sh\n" | tee -a ~/.bashrc
RUN echo "\n. $HOME/.asdf/completions/asdf.bash\n" | tee -a ~/.bashrc

# Setup starship.
RUN echo 'eval "$(starship init bash)"' | tee -a ~/.bashrc

# Setup direnv.
RUN echo 'eval "$(direnv hook bash)"' | tee -a ~/.bashrc

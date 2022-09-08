#! /usr/bin/env python3

flatpak-builder --force-clean --user --install build/ com.github.EEmodders.EEstudioII.yml
flatpak build-bundle ~/.local/share/flatpak/repo EEStudioII.flatpak com.github.EEmodders.EEstudioII

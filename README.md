# Empire Earth Studio II

A better version of the original EEStudio, that hopefully will finally no longer be used. :)

### How to install

- Download the version you need from the [release page](https://github.com/EE-modders/Empire-Earth-Studio-2/releases).
- Run the portable version or install it using the installer.

A tutorial on how to use is in the works, but it should be self explanatory.

### How to run from source code

```bash
git clone https://github.com/EE-modders/Empire-Earth-Studio-2.git
git submodule update --init
cd Empire-Earth-Studio-2/src
pip3 install -r requirements.txt

# run it
python3 EEStudio2.py
```

### Known limitations / bugs

- the SST Slicer does sometimes produce black borders when using JOIN
  (It should however work with the default split of 4x3, which EE is using)
- on the Slicer tab Drag & Drop does not work (use the select button instead)

### Reporting

If you find any bug or if you want to request a new feature, please feel free to

- [create a new issue](https://github.com/EE-modders/Empire-Earth-Studio-2/issues) on GitHub or
- join our [Empire Earth: Reborn Discord](https://discord.gg/BjUXbFB) server

<iframe src="https://discord.com/widget?id=614154073759023104&theme=dark" width="350" height="350" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>

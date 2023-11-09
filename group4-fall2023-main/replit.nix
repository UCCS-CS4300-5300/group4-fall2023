{ pkgs }: {
  deps = [
    pkgs.python39Packages.django
    pkgs.python39Packages.pip
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nodePackages.typescript-language-server  
  ];
}
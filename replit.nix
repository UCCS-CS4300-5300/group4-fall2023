{ pkgs }: {
  deps = [
    pkgs.python38Packages.coverage
    pkgs.httpie
    pkgs.python39Packages.django
    pkgs.python39Packages.pip
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nodePackages.typescript-language-server  
  ];
}
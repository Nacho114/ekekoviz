{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.numpy
    pkgs.python311Packages.pandas
    pkgs.python311Packages.plotly
    pkgs.python311Packages.yfinance
    pkgs.python311Packages.scipy
    pkgs.python311Packages.matplotlib
    # For packaging
    pkgs.python311Packages.packaging    
    pkgs.python311Packages.virtualenv
    pkgs.python311Packages.setuptools   
  ];

  shellHook = ''
    # Create a virtual environment and activate it
    if [ ! -d ".venv" ]; then
      python -m virtualenv .venv
    fi
    source .venv/bin/activate
  '';
}

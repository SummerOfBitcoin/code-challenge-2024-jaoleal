{
 description = "Flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, rust-overlay, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      overlays = [
        (import rust-overlay)
      ];
      pkgs = import nixpkgs {
        inherit system overlays;
      };
    in
    with pkgs;
    {
      devShells.default = mkShell {
        buildInputs = [
          python310Packages.pytest
          python3
          openssl
          pkg-config
          rust-bin.stable.latest.default
        ];
      };
    }
  );
}
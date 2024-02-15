# User-specific variables
BUILD_DIR="bld"
INSTALL_DIR="eclm"

# Run cmake
cmake -S src -B "$BUILD_DIR" \
      -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
      -DCMAKE_C_COMPILER=mpicc \
      -DCMAKE_Fortran_FLAGS="-fallow-argument-mismatch -fallow-invalid-boz" \
      -DCMAKE_Fortran_COMPILER=mpifort

cd bld
make -j8

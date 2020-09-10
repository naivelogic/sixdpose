export SRC=http://ptak.felk.cvut.cz/6DB/public/bop_datasets
wget $SRC/ycbv_base.zip         # Base archive with dataset info, camera parameters, etc.
wget $SRC/ycbv_models.zip       # 3D object models.
wget $SRC/ycbv_test_all.zip     # All test images ("_bop19" for a subset used in the BOP Challenge 2019/2020).
wget $SRC/ycbv_train_pbr.zip    # PBR training images (rendered with BlenderProc4BOP).

unzip ycbv_base.zip                 # Contains folder "ycbv".
unzip ycbv_models.zip -d ycbv     # Unpacks to "ycbv".
unzip ycbv_test_all.zip -d ycbv   # Unpacks to "ycbv".
unzip ycbv_train_pbr.zip -d ycbv  # Unpacks to "ycbv".
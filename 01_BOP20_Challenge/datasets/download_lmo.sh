export SRC=http://ptak.felk.cvut.cz/6DB/public/bop_datasets
wget $SRC/lmo_base.zip         # Base archive with dataset info, camera parameters, etc.
wget $SRC/lmo_models.zip       # 3D object models.
wget $SRC/lmo_test_all.zip     # All test images ("_bop19" for a subset used in the BOP Challenge 2019/2020).
wget $SRC/lmo_train.zip    # PBR training images (rendered with BlenderProc4BOP).

unzip lmo_base.zip               # Contains folder "lmo".
unzip lmo_models.zip -d lmo     # Unpacks to "lmo".
unzip lmo_test_all.zip -d lmo   # Unpacks to "lmo".
unzip lmo_train.zip -d lmo  # Unpacks to "lmo".



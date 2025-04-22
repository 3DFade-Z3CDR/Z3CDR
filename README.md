To mitigate potential misuse and ensure the security of cloud manufacturing systems, the source code for SHIE3D model is not publicly released. However, we provide a detailed description of the attack methodology in the paper to support reproducibility. Therefore, here we have only made the attack dataset and the defense code for Z3CDR publicly available.
# Z3CDR
Z3CDR combines Zero Trust (ZT) and Content Disarm and Reconstruction (CDR) technologies. Based on the assumption of distrust of all file sources, it believes that every file may contain potential threats. The following is the relevant source code.

## 1.Z3_CDR_3MF

### Build_repetition_CDR.py

Detect and defend against build_repetition and model_overlap attacks in 3mf files

### Circular_reference_CDR.py

Detect  against circular_reference attacks in 3mf files

### Hollow_Embedding_CDR.py

Detect and defend against hollow_embedding attacks in 3mf files

### Steganographic_CDR.py

Detect and defend against Steganographic attacks (include Weak Attack、Regular Attack、Strong Attack) in 3mf files

### catalog_examine.py

Check if the 3mf file format is correct

### file_handle.py

Process and extract some information from 3mf files

### 3MF_test.py

Detect and defend against attacks on 3mf files, these attacks include Build_repetition、Model_overlap、Circular_reference、Hollow_Embedding、Steganographic(Weak Attack、Regular Attack、Strong Attack)



## 2.Z3_CDR_STL

### build_repetition_CDR.py

Detect and defend against **build_repetition** and model_overlap attacks in STL files

### model_overlap_CDR.py

Detect and defend against build_repetition and **model_overlap** attacks in STL files

### Steganographic_CDR.py

Detect and defend against Steganographic attacks (include Weak Attack、Regular Attack、Strong Attack) in STL files

### STL_test.py

Detect and defend against attacks on STL files, these attacks include Build_repetition、Model_overlap、Steganographic(Weak Attack、Regular Attack、Strong Attack)



## 3.Z3_CDR_OBJ

### build_repetition_CDR.py

Detect and defend against **build_repetition** and model_overlap attacks in OBJ files

### model_overlap_CDR.py

Detect and defend against build_repetition and **model_overlap** attacks in OBJ files

### Steganographic_CDR.py

Detect and defend against Steganographic attacks (include Weak Attack、Regular Attack、Strong Attack) in OBJ files

### OBJ_test.py

Detect and defend against attacks on OBJ files, these attacks include Build_repetition、Model_overlap、Steganographic(Weak Attack、Regular Attack、Strong Attack)



## 4.Z3_CDR_STEP

### build_repetition_CDR.py

Detect and defend against **build_repetition** and model_overlap attacks in STEP files

### model_overlap_CDR.py

Detect and defend against build_repetition and **model_overlap** attacks in STEP files

### Steganographic_CDR.py

Detect and defend against Steganographic attacks (include Weak Attack、Regular Attack、Strong Attack) in STEP files

### STEP_test.py

Detect and defend against attacks on STEP files, these attacks include Build_repetition、Model_overlap、Steganographic(Weak Attack、Regular Attack、Strong Attack)




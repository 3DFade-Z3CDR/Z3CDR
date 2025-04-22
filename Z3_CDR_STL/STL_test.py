import Steganographic_CDR as SD
import build_repetition_CDR as RSD
from CDR_STL import Overlap_defense as OLD
import time

if __name__ == '__main__':

        start_time = time.time()
        dection_times = []

        for i in range(1,101):
            # Establish the file path: take Build_repetition as an example. Assume there are 100 STL files in the folder.
            infile = "../Dataset/attack_stl/Build Repetition Attack/rebuild_data_"+str(i)+".stl"
            outfile = "Z3_CDR_STL/Defense_STL/defense_data_"+str(i)+".stl"

            SGOP_res=SD.Steganographic_detection(infile)#Judge whether there is a Steganographic attack
            if SGOP_res:
                SD.Steganographic_Defense(infile,outfile)
            else:
                Rebuild_res=RSD.build_repetition_dection(infile)#Judge whether there is a rebuild_repetition or model_overlap attack
                if Rebuild_res:
                    RSD.build_repetition_defense(infile,outfile)
        end_time = time.time()

        print("Average processing time", round((end_time - start_time) / 100, 3))
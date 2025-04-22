import model_overlap_CDR as OD
import Steganographic_CDR as SD

import time

if __name__ == '__main__':

        start_time = time.time()
        dection_times = []
        for i in range(1,101):
            # Establish the file path: take Build_repetition as an example. Assume there are 100 OBJ files in the folder.

            infile = "../Dataset/attack_obj/Build Repetition Attack/rebuild_data_"+str(i)+".obj"
            outfile = "Z3_CDR_OBJ/Defense_OBJ/defense_data_"+str(i)+".obj"

            SGOP_res=SD.Steganographic_Dection(infile)#Judge whether there is a Steganographic attack
            if SGOP_res:
                SD.Steganographic_Defense(infile,outfile)
            else:
                unique_res=OD.model_overlap_dection(infile)#Judge whether there is a rebuild_repetition or model_overlap attack
                if unique_res:
                    OD.model_overlap_defense(infile,outfile)
                else:
                    pass
        end_time = time.time()

        print("Average processing time", round((end_time - start_time) / 100, 3))

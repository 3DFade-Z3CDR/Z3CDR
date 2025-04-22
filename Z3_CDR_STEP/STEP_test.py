import Steganographic_CDR as SD
import build_repetition_CDR as RSD
import time

if __name__ == '__main__':

        start_time = time.time()
        dection_times = []

        for i in range(1,101):
            # Establish the file path: take Build_repetition as an example. Assume there are 100 STEP files in the folder.
            infile = "../Dataset/attack_step/Build Repetition Attack/rebuild_data_"+str(i)+".step"
            outfile = "Z3_CDR_STEP/Defense_STEP/defense_data_"+str(i)+".step"

            SGOP_res=SD.Steganographic_detection(infile)#Judge whether there is a Steganographic attack
            if SGOP_res:
                SD.Steganographic_defense(infile,outfile)
            else:
                Rebuild_res=RSD.build_repetition_dection(infile)#Judge whether there is a rebuild_repetition or model_overlap attack
                if Rebuild_res:
                    RSD.build_repetition_defense(infile,outfile)
        end_time = time.time()

        print("Average processing time", round((end_time - start_time) / 100, 3))
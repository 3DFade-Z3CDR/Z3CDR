import Circular_reference_CDR as ie
import catalog_examine as ce
import Steganographic_CDR as SC
import Build_repetion_CDR as RD
import Hollow_Embedding_CDR as MC
import time


if __name__ == '__main__':

        start_time = time.time()
        dection_time=0
        for i in range(1,101):
            # Establish the file path: take Build_repetition as an example. Assume there are 100 3mf files in the folder.
            inputfile="../Dataset/attack_3mf/Build Repetition Attack/attack_data_"+str(i)+".3mf"
            defense_dir="Z3_CDR_3MF/Denfense_3MF/defense_temp_dir"
            defense_3mf="Z3_CDR_3MF/Denfense_3MF/defense_data_"+str(i)+".3mf"

            # Check whether the format is correct
            format_res=ce.check_3mf_format(inputfile,defense_dir)  # Check whether the format is correct
            if format_res:  # If the format is correct, proceed with iterative detection
                model_file=ce.find_3dmodel_file(defense_dir)

                # Detect whether there is an excessive iteration of components. True means within limit, False means exceeded.
                if ie.check_circular_reference_depth(model_file,max_depth=5):

                    # Detect if there is a steganographic attack
                    SGOP_res = SC.Steganographic_dection_model(model_file)
                    if SGOP_res:
                        SC.Steganographic_defense_model(model_file, model_file)
                    else:
                        # Detect if there is a build repetition or model overlapping attack
                        rebuild_res=RD.Build_repetition_dection(model_file)
                        if rebuild_res:
                            RD.Build_repetition_defense(model_file,model_file)
                        else:
                            # Detect if there is a mosaic attack
                            mosaic_res=MC.UI_disarm(model_file)
                            if mosaic_res:
                                MC.Hollow_Embedding_defense(model_file,model_file,mosaic_res)
                            else:
                                pass
                elif ie.check_circular_reference_depth(model_file,max_depth=15):
                    print("Exceeded 5 levels of iteration, please note.")
                else:
                    end_time=time.time()
                    print(end_time-start_time)
                    raise EOFError("Exceeded 20 levels of iteration")
            else:
                raise EOFError("file exist circular reference error")

        end_time = time.time()
        print("Average processing time", round((end_time-start_time)/100, 3))

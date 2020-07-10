import writeprocessingfile
import processmodel

show_acc_sample_data = True
updateSampleFiles = False


writeprocessingfile.writeProcessingFile(updateSampleFiles)
processmodel.processingModel(show_acc_sample_data)


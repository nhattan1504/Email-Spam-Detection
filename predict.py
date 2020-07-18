import writeprocessingfile
import processmodel

show_acc_sample_data = False
updateSampleFiles = False


writeprocessingfile.writeProcessingFile(updateSampleFiles)
processmodel.processingModel(show_acc_sample_data)


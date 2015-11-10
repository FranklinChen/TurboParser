﻿import sys
import os
import subprocess
import time

NumberOfRuns=1
NumberWarmUps=0


#Programs = ['C:\\Projects\\TurboParser_DN\\vsprojects\\x64\\Release\\turbo_morphological_tagger.exe'] #create a copy in other folder to allow development of the code without interfering with the experiment
Programs = ['C:\\Projects\\TurboParser_DN\\scripts_morph\\turbo_morphological_tagger.exe']


Languages = ['basque',
'bulgarian',
'croatian',
'czech',
'danish',
'english',
'finnish',
'greek',
'hungarian',
'italian',
'swedish']

TrainFiles_template      = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_data\\*__LANGUAGE__*-ud-train.conllu'] #Replace *__LANGUAGE__* by Languages[i]
TestFiles_template       = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_data\\*__LANGUAGE__*-ud-test.conllu'] #Replace *__LANGUAGE__* by Languages[i]
ModelFiles_template      = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_models\\*__LANGUAGE__*_morphtagger.model_mo*__MARKOV_ORDER__*_feat*__FEATURES__*_trc*__REGCONST__*_p*__PREFIX__*s*__SUFFIX__*'] #Replace '*__LANGUAGE__*','__MARKOV_ORDER__*' '*__FEATURES__*', '*__REGCONST__*', '*__PREFIX__*', '*__SUFFIX__*'
PredictionFiles_template = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_out\\*__LANGUAGE__*-train-test.morphtagger.model_mo*__MARKOV_ORDER__*_feat*__FEATURES__*_trc*__REGCONST__*_p*__PREFIX__*s*__SUFFIX__*.predicted'] 
TrainFiles               = []     
TestFiles                = []  
ModelFiles               = []
PredictionFiles          = []

MorphFeatureSelection       = ['0', '1', '2'] #--morph_tagger_large_feature_set=0
TrainAlgorithm              = ['svm_mira'] #--train_algorithm=svm_mira
TrainRegularizationConstant = ['1.0', '0.1', '0.01'] #--train_regularization_constant=0.01 
TrainEpochs                 = ['20'] #--train_epochs=20 
SequenceModelType           = ['0'] #--sequence_model_type=0 
FormCutoff                  = ['0'] #--form_cutoff=0 
PrefixLength                = ['0','2','3'] #--prefix_length=3 
SuffixLength                = ['0','2','3'] #--suffix_length=3 
#--logtostderr              

OutputDesiredPrefix     = "turbo_morphological_tagger_run"
OutputFolder            = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_out\\'] 
OutputFolderBenchmarks  = ['C:\\Projects\\TurboParser_DN\\data_local\\morph_out\\']

if not os.path.exists(os.path.dirname(OutputFolderBenchmarks[0])):
    os.makedirs(os.path.dirname(OutputFolderBenchmarks[0]))

timestr = time.strftime("%Y%m%d-%H%M%S")
csv = open(OutputFolderBenchmarks[0]+OutputDesiredPrefix+timestr+".csv","w")
log = open(OutputFolderBenchmarks[0]+OutputDesiredPrefix+timestr+".log","w")
err = open(OutputFolderBenchmarks[0]+OutputDesiredPrefix+timestr+".err","w")
pylog = open(OutputFolderBenchmarks[0]+OutputDesiredPrefix+timestr+".pylog","w")


 
string_to_write=""
string_to_write=string_to_write+"Program, Language, Features, Markov Order, Train Algorithm, Regularization Constant, Train Epochs, Form cutoff, Prefix Length, Suffix Length"
#string_to_write=string_to_write+", "+"Training time"  #Commented for Windows execution; turn on in Linux environment
if NumberOfRuns == 1:
    #string_to_write=string_to_write+", "+"Run(Test) time"  #Commented for Windows execution; turn on in Linux environment
    string_to_write=string_to_write+", "+"CorrectPredict"
    string_to_write=string_to_write+", "+"Accuracy"
    string_to_write=string_to_write+", "+"Speed (token/sec)"
else:
    for i in range(NumberOfRuns):
        #string_to_write=string_to_write+", "+"Run(Test) time["+str(i)+"]"  #Commented for Windows execution; turn on in Linux environment
        string_to_write=string_to_write+", "+"CorrectPredict["+str(i)+"]"
        string_to_write=string_to_write+", "+"Accuracy["+str(i)+"]"
        string_to_write=string_to_write+", "+"Speed["+str(i)+"] (token/sec)"
     
string_to_write=string_to_write+"\n"
csv.write(string_to_write)
     
for program in Programs:
    for language in Languages:    
        for features in MorphFeatureSelection:
            for sequence_model_type in SequenceModelType:
                for train_algorithm in TrainAlgorithm:
                    for train_regularization_constant in TrainRegularizationConstant:
                        for train_epochs in TrainEpochs:
                            for form_cutoff in FormCutoff: 
                                for prefix_length in PrefixLength:
                                    for suffix_length  in  SuffixLength:
                        
                                        TrainFile       = TrainFiles_template[0]
                                        TrainFile       = TrainFile.replace('*__LANGUAGE__*', language)

                                        TestFile        = TestFiles_template[0]
                                        TestFile        = TestFile.replace('*__LANGUAGE__*', language)
                                        
                                        ModelFile       = ModelFiles_template[0]
                                        ModelFile       = ModelFile.replace('*__LANGUAGE__*', language)
                                        ModelFile       = ModelFile.replace('*__MARKOV_ORDER__*', sequence_model_type)
                                        ModelFile       = ModelFile.replace('*__FEATURES__*', features)
                                        ModelFile       = ModelFile.replace('*__REGCONST__*', train_regularization_constant)
                                        ModelFile       = ModelFile.replace('*__PREFIX__*', prefix_length)
                                        ModelFile       = ModelFile.replace('*__SUFFIX__*', suffix_length)
                                        
                                        PredictionFile  = PredictionFiles_template[0]
                                        PredictionFile  = PredictionFile.replace('*__LANGUAGE__*', language)
                                        PredictionFile  = PredictionFile.replace('*__MARKOV_ORDER__*', sequence_model_type)
                                        PredictionFile  = PredictionFile.replace('*__FEATURES__*', features)
                                        PredictionFile  = PredictionFile.replace('*__REGCONST__*', train_regularization_constant)
                                        PredictionFile  = PredictionFile.replace('*__PREFIX__*', prefix_length)
                                        PredictionFile  = PredictionFile.replace('*__SUFFIX__*', suffix_length)
                                        
                                        
                                        #TRAIN
                                        command = []
                                        #command.append("time -p") #Commented for Windows execution; turn on in Linux environment
                                        command.append(program)
                                        command.append("--train")
                                        command.append("--file_train="+TrainFile)
                                        command.append("--file_model="+ModelFile)
                                        command.append("--train_algorithm="+train_algorithm)
                                        command.append("--train_regularization_constant="+train_regularization_constant)
                                        command.append("--train_epochs="+train_epochs)
                                        command.append("--sequence_model_type="+sequence_model_type)
                                        command.append("--form_cutoff="+form_cutoff)
                                        command.append("--prefix_length="+prefix_length)
                                        command.append("--suffix_length="+suffix_length)
                                        command.append("--morph_tagger_large_feature_set="+features)
                                        command.append("--logtostderr")


                                        print "Executing: " + ' '.join(command)
                                        sys.stdout.flush()
                                     
                                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        (stdout__output,stderr_output) = process.communicate()
                                        print "Finished executing: " + ' '.join(command)
                                        sys.stdout.flush()
                                            
                                        # print "- - - * * * - - -"
                                        stdout__output = stdout__output.splitlines()
                                        for line in stdout__output:
                                            log.write(line)
                                            # print line.rstrip("\n")
                                                
                                        # print "- - - * * * - - -"
                                        stderr_output = stderr_output.splitlines()
                                        for line in stderr_output:
                                            err.write(line)
                                            # print line.rstrip("\n")                                        
                                            where=line.find("Training took ")
                                            if where != -1:
                                                print line[where:]
                                                sys.stdout.flush()
                                                training_time = float(line[where+len("Training took "):len(line)-len(" sec.")])
                                                print       "Training time = "+str(training_time)+" seconds\n"
                                                sys.stdout.flush()
                                                pylog.write("Training time = "+str(training_time)+" seconds\n")
                                                log.write(  "Training time = "+str(training_time)+" seconds\n")

                                            if line[0:4]=="real":
                                               train_time = float(line[5:])
                                               print       "time of execution = "+str(train_time)+" seconds\n"
                                               sys.stdout.flush()
                                               pylog.write("time of execution = "+str(train_time)+" seconds\n")
                                               log.write(  "time of execution = "+str(train_time)+" seconds\n")
                                            # print line
                                        
                                        #TEST
                                        command = []
                                        #command.append("time -p") #Commented for Windows execution; turn on in Linux environment
                                        command.append(program)        
                                        command.append("--test")        
                                        command.append("--evaluate")
                                        command.append("--file_model="+ModelFile)
                                        command.append("--file_test="+TestFile)
                                        command.append("--file_prediction="+PredictionFile)    
                                        command.append("--logtostderr")


                                        print "Executing: " + ' '.join(command)
                                        sys.stdout.flush()
                                        
                                    
                                        #warm-up X iterations
                                        for iteration in range(0,NumberWarmUps):
                                            #run program
                                            process=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            (stdout__output,stderr_output) = process.communicate()
                                            print "Finished executing: " + ' '.join(command)
                                            sys.stdout.flush()
                                    
                                        test_time=[]
                                        correct_predictions=[]
                                        accuracy=[]
                                        tagspeed=[]
                                        for iteration in range(NumberOfRuns):
                                            print       "\n"
                                            pylog.write("\n")
                                            log.write(  "\n")
                                            err.write(  "\n")
                                            if NumberOfRuns > 1:
                                                print       "\n**** ITER "+str(iteration)+" ****\n"
                                                sys.stdout.flush()
                                                pylog.write("\n**** ITER "+str(iteration)+" ****\n")
                                                log.write(  "\n**** ITER "+str(iteration)+" ****\n")
                                                err.write(  "\n**** ITER "+str(iteration)+" ****\n")
                                            print       ' '.join(command)
                                            sys.stdout.flush()
                                            pylog.write(' '.join(command) )
                                            log.write(  ' '.join(command) )
                                            err.write(  ' '.join(command) )
                                            #run program
                                            process=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            (stdout__output,stderr_output) = process.communicate()
                                            print "Finished executing: " + ' '.join(command)
                                            sys.stdout.flush()
                                            
                                            # print "- - - * * * - - -"
                                            stdout__output = stdout__output.splitlines()                                      
                                            for line in stdout__output:
                                                log.write(line)
                                                # print line.rstrip("\n")
                                            # print "- - - * * * - - -"
                                            stderr_output = stderr_output.splitlines()
                                            for line in stderr_output:
                                                err.write(line)
                                                # print line.rstrip("\n")
                                                where=line.find("Correct predictions:")  
                                                if where != -1:    
                                                    print line[where:]
                                                    sys.stdout.flush()
                                                    correct_predictions.append( line[where+len("Correct predictions: "):] )
                                                    print       "Correct predictions: "+correct_predictions[iteration]+"\n"
                                                    sys.stdout.flush()
                                                    pylog.write("Correct predictions: "+correct_predictions[iteration]+"\n")
                                                    log.write(  "Correct predictions: "+correct_predictions[iteration]+"\n")                                              
                                                
                                                
                                                where=line.find("Tagging accuracy: ")
                                                if where != -1:
                                                    print line[where:]
                                                    sys.stdout.flush()
                                                    accuracy.append( float(line[where+len("Tagging accuracy: "):]) )
                                                    print       "Tagging accuracy = "+str(accuracy[iteration])+"\n"
                                                    sys.stdout.flush()
                                                    pylog.write("Tagging accuracy = "+str(accuracy[iteration])+"\n")
                                                    log.write(  "Tagging accuracy = "+str(accuracy[iteration])+"\n")
                                               
                                               
                                                where=line.find("Tagging speed: ")  
                                                if where != -1:    
                                                    print line[where:]
                                                    sys.stdout.flush()
                                                    tagspeed.append( float(line[where+len("Tagging speed: "):len(line) - len(" tokens per second.")]) )
                                                    print       "Tagging speed = "+str(tagspeed[iteration])+"\n"
                                                    sys.stdout.flush()
                                                    pylog.write("Tagging speed = "+str(tagspeed[iteration])+"\n")
                                                    log.write(  "Tagging speed = "+str(tagspeed[iteration])+"\n")
                                                
                                                if line[0:4]=="real":
                                                    test_time.append( float(line[5:]) )
                                                    print       "time of execution = "+str(test_time[iteration])+" seconds\n"
                                                    sys.stdout.flush()
                                                    pylog.write("time of execution = "+str(test_time[iteration])+" seconds\n")
                                                    log.write(  "time of execution = "+str(test_time[iteration])+" seconds\n")
                                                # print line    
                                                
                                        string_to_write=""
                                        string_to_write=string_to_write+program
                                        string_to_write=string_to_write+","+language
                                        string_to_write=string_to_write+","+features
                                        string_to_write=string_to_write+","+sequence_model_type
                                        string_to_write=string_to_write+","+train_algorithm
                                        string_to_write=string_to_write+","+train_regularization_constant
                                        string_to_write=string_to_write+","+train_epochs
                                        string_to_write=string_to_write+","+form_cutoff
                                        string_to_write=string_to_write+","+prefix_length
                                        string_to_write=string_to_write+","+suffix_length
                                        
                                        
                                        #string_to_write=string_to_write+","+str(train_time) #Commented for Windows execution; turn on in Linux environment

                                        for i in range(NumberOfRuns):
                                            #string_to_write=string_to_write+","+str(test_time[i]) #Commented for Windows execution; turn on in Linux environment
                                            string_to_write=string_to_write+","+str(correct_predictions[i])
                                            string_to_write=string_to_write+","+str(accuracy[i])
                                            string_to_write=string_to_write+","+str(tagspeed[i])
                                        string_to_write=string_to_write+"\n"
                                        
                                        csv.write(string_to_write)

                                        csv.flush()
                                        log.flush()
                                        pylog.flush()
                                        err.flush()
                                                   
#CLOSING						
csv.close()
print "Script finished\n"
log.write("Script finished\n")
pylog.write("Script finished\n")
log.close()
pylog.close()
err.close()

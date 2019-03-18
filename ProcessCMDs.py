import ParseFunctions as pf
import ProcessRuns as pr
import AllModules as am


################################################################################################################################################################################################################                                                                         
################################################################################################################################################################################################################                                                                         
##################################These Functions get run lists for various processes from the run table and returns the list of the respective process running commands #######################################
################################################################################################################################################################################################################                                                                         ################################################################################################################################################################################################################                                                                                                           


def TrackingCMDs(Debug):

    RunList, FieldIDList = pr.TrackingRuns(False)
    TrackingCMDList = []
    ResultFileLocationList = []

    if RunList:
        
        for run in RunList: 

            TrackingCMDList.append('source %s %d' % (am.HyperscriptPath, run))
            ResultFileLocationList.append(am.BaseTrackDirLocal + 'Run%d_CMSTiming_converted.root' % run)

    return TrackingCMDList, ResultFileLocationList, RunList, FieldIDList


def ConversionCMDs(Debug):

    RunList, FieldIDList = pr.ConversionRuns(False)
    ConversionCMDList = []
    ResultFileLocationList = []

    if RunList:
        
        for run in RunList: 

            ConversionCMDList.append(am.ConversionCMD + str(run))
            ResultFileLocationList.append(am.RawStageTwoLocalPathScope + 'run_scope' + str(run) + '.root')

    return ConversionCMDList, ResultFileLocationList, RunList, FieldIDList


def TimingDAQCMDs(SaveWaveformBool, Version, Debug):

    RunList, FieldIDList, DigitizerList, RedoList, VersionList = pr.TimingDAQRuns(False)
    DatToRootCMDWithTracksList = []
    DatToRootCMDWithoutTracksList = []
    ResultFileLocationList = []

    if RunList:
        
        for run in RunList: 

            RecoLocalPath = None
            RawLocalPath = None
            Digitizer = []
            Index = RunList.index(run)
            Digitizer = (DigitizerList[Index])[0]

            if RedoList[Index] == 'Redo': 
                Version = VersionList[Index]
            else: 
                Version = Version

            RecoBaseLocalPath = am.RecoBaseLocalPath + Digitizer+ '/' + Version + '/'
            if not am.os.path.exists(am.RecoBaseLocalPath): am.os.system('mkdir %s' % am.RecoBaseLocalPath)

            if Digitizer == 'VME' or Digitizer == 'DT5742':
                am.RawBaseLocalPath = am.RawBaseLocalPath + Digitizer + '/' + Version + '/' 
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(am.RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(am.RawBaseLocalPath + '*_Run*')] 
                RawLocalPath = ListRawFilePath[ListRawRunNumber.index(run)]
                RecoLocalPath = am.RecoBaseLocalPath + RawLocalPath.split(".dat")[0].split("%s/" % Version)[1] + '.root'                                            
 
            elif Digitizer == 'TekScope':
                Digitizer = 'NetScopeStandalone'
                RawLocalPath = am.RawStageTwoLocalPathScope + 'run_scope' + str(run) + '.root'                                      
                RecoLocalPath = am.RecoBaseLocalPath + Digitizer + '/' + Version + '/' + 'run_scope' + str(run) + '_converted.root' 

            ResultFileLocationList.append(RecoLocalPath)
            ConfigFilePath = am.ConfigFileBasePath + Digitizer + '_%s.config' % Version
            DatToRootCMD = './' + Digitizer + 'Dat2Root' + ' --config_file=' + ConfigFilePath + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath
            if SaveWaveformBool: DatToRootCMD = DatToRootCMD + ' --save_meas'
            DatToRootCMDWithoutTracksList.append(DatToRootCMD)

            TrackFilePathLocal = am.BaseTrackDirLocal + 'Run%i_CMSTiming_converted.root' % run
            DatToRootCMDWithTracksList.append(DatToRootCMD + ' --pixel_input_file=' + TrackFilePathLocal)                                        
        
        return DatToRootCMDWithTracksList, DatToRootCMDWithoutTracksList, ResultFileLocationList, RunList, FieldIDList




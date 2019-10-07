#from niveristand import nivs_rt_sequence, NivsParam, realtimesequencetools
#Import the next two elements to be able to read/write VeriStand channels and wait
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait

#Import the next elements to be able to create a logging specification
import clr
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
from NationalInstruments.VeriStand.ClientAPI import Factory
from NationalInstruments.VeriStand.ClientAPI import Logging
from NationalInstruments.VeriStand.ClientAPI.Logging import *

from System import Array

####################
###Setup logging ###

#Open Data Logging Manager Reference. We use localhost because logging takes place in the local computer
Data_Logging_Manager_Ref = Factory().GetIDataLogging("localhost")

#New TDMS Log File. First input is path to logging file. Second input is fileConflictOperation. 0 means create a new file with unique name
TDMSLogFile_Ref = TdmsLogFile(r"C:\Users\chericks\Documents\VeriStand Projects\Engine Demo\Logs\myLog.tdms",0)

#Add TDMS Group and one channel. Repeat for as many groups and channels.
Group_ref = TdmsChannelGroup("myGroup")
Channel_ref = TdmsChannel("myChannel","Aliases/ActualRPM")
#Add channel to group
Group_ref.AddChannel(Channel_ref)

#Add group to TDMS file
TDMSLogFile_Ref.AddChannelGroup(Group_ref)

#New Data Logging Specification (TDMS)
Logging_Specification_Ref = DataLoggingSpecification(TDMSLogFile_Ref)

#Configure custom logging rate to 20 Hz
Logging_Specification_Ref.LogDataAtTargetRate = False
Logging_Specification_Ref.CustomRate = 20

#Set Start Trigger to Analog Trigger
#trigger = DefaultTrigger(True)  #(Start Immediately, do not wait for any trigger)

trigger = AnalogEdgeTrigger("Aliases/ActualRPM",2800,0,True)
#(Trigger channel, threshold, edge: rising 0 and falling 1,strict edge bool)

#Assign trigger to spec
Logging_Specification_Ref.StartTrigger = trigger

#Set Pre-trigger duration, retriggerable flag and file segmenting if desired
Logging_Specification_Ref.PreTriggerDuration = 1
Logging_Specification_Ref.Retriggerable = True
Logging_Specification_Ref.SegmentFileOnTrigger = True

#Set Stop Trigger (Duration)
Logging_Specification_Ref.StopTrigger = DefaultTrigger(True)
Logging_Specification_Ref.PostTriggerDuration = 4

#Start Data Logging Session
Data_Logging_Manager_Ref.StartDataLoggingSession("myLoggingSession",Logging_Specification_Ref)

#################################################
###Changes channel values, wait and reset ###

#Prepare values that will be assigned
engine_power = BooleanValue(True)
desired_rpm = DoubleValue(3000)
wait_time = DoubleValue(10)

# You can access a channel with a ChannelReference
engine_power_chan = ChannelReference('Aliases/EnginePower')
desired_rpm_chan = ChannelReference('Aliases/DesiredRPM')
engine_power_chan.value = engine_power.value
desired_rpm_chan.value = desired_rpm.value
wait(wait_time.value)
engine_power_chan.value = False
desired_rpm_chan.value = 0

###############################################
#Stop Data Logging Session
logs_array = ["logs"]
Data_Logging_Manager_Ref.StopDataLoggingSession("myLoggingSession",True,Array[str](logs_array))


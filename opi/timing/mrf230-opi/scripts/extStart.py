#!/usr/bin/env python
import json
import epics
import sys

print 'Loading configuration ' + sys.argv[1]
sys.stdout.flush()

prefix = 'GEN-TMG-'
evg_name = 'EVG01'
evg = "".join((prefix, evg_name))

fps=('UNIV0','UNIV1','UNIV2','UNIV3')
no_evr = []

loadsts = epics.caget("".join((evg,':SoftSeq-1-Load-RB')))
if loadsts == 0:
	try:
		with open(sys.argv[1], 'r') as infile:
			data=json.load(infile)
		evrs=map(str,data.keys())
		evrs.remove('EVG')
		evrs.sort()
		
		toes = data['EVG']['TOE_TE'].keys()
		toes.sort()
		
		### EVG parameters
		EVG_units = data['EVG']['Units'] 
		EVG_toe = [float(i) for i in toes]
		EVG_te = []
		for i in range(len(toes)):
			EVG_te.append(data['EVG']['TOE_TE'][toes[i]])
 
		### caput into EPICS PVs 
		epics.caput("".join((evg,':SoftSeq-1-EvtCode-SP')), EVG_te)
		epics.caput("".join((evg,':SoftSeq-1-Timestamp-SP')), EVG_toe)
		epics.caput("".join((evg,':SoftSeq-1-TsResolution-Sel')), EVG_units)
		for i in evrs: # EVR
			pref=''.join((prefix,i))
			check_pv = epics.PV("".join((pref,":Ena-Sel")))
			if (check_pv.status is None):
				print 'Cannot connect to ' + i
				sys.stdout.flush()
				no_evr.append(i)
			else:
				for j in fps: # Front panel 0 - 3
					epics.caput("".join((pref,":Pul",j[-1],"-Evt-Trig0-SP")), data[i][j]['Event'])
					epics.caput("".join((pref,":Pul",j[-1],"-Delay-SP")), data[i][j]['Delay'])
					epics.caput("".join((pref,":Pul",j[-1],"-Width-SP")), data[i][j]['Width'])
					epics.caput("".join((pref,":Pul",j[-1],"-Polarity-Sel")), data[i][j]['Polarity'])
					if (int(data[i][j]['Polarity']) != 0) and (int(data[i][j]['Polarity']) != 1):
						print 'ERROR in ' + "".join((pref,":Pul",j[-1],"-Polarity-Sel"))
		
		if (len(no_evr) > 0):
			if (len(no_evr) > 1):				
				print 'Cannot connect to EVRs ' + str(no_evr)
				sys.stdout.flush()
			print "Do you want to continue? (yes/no)"
			sys.stdout.flush()
			cont = raw_input()
			
			while ((not cont == 'yes') and (not cont == 'no')):
				print "Invalid input. Please enter 'yes' or 'no'."
				sys.stdout.flush()
				cont = raw_input()
			
			if (cont == 'yes'):
				evrs = [x for x in evrs if x not in no_evr]
			
			elif (cont == 'no'):
				print "Exiting"
				sys.stdout.flush()
				sys.exit()
		
		epics.caput("".join((evg,':SoftSeq-1-Commit-Cmd')), 1)
		with open(sys.argv[2], 'w') as outfile:
					outfile.write(sys.argv[1])	
		
	except Exception:
		with open(sys.argv[2], 'w') as outfile:
			outfile.write('Error')
		raise
		
	commit = epics.caget("".join((evg,':SoftSeq-1-Commit-RB')))
	if commit == 1:
		epics.caput("".join((evg,':SoftSeq-1-Load-Cmd')), 1)
		epics.caput("".join((evg,':SoftSeq-1-Enable-Cmd')), 1)
		with open(sys.argv[3],'w') as outfile2:
			outfile2.write(" ".join(evrs))
	
		print 'Configured \'' + str(evg_name) + '\' and ' + str(evrs).strip('[]') + '.'
		print 'Console output written to ' + sys.argv[4]
		print 'Done!'
	else:
		print 'Error. Please check your configuration.'
		with open(sys.argv[2], 'w') as outfile:
			outfile.write('Error')
elif loadsts==1:
	print 'WARNING: Sequence is already running.'	
else:
	print 'Please check your connection.'
	print 'Exiting'

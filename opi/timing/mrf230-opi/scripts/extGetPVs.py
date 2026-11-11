#!/usr/bin/env python
import json
import epics
import sys

### caget PV values and store them in json file

with open(sys.argv[3], 'r') as infile:
	evrs0=infile.read()
evrs = evrs0.split(' ')

prefix = 'GEN-TMG-'
evg_name = 'EVG01'
evg = "".join((prefix, evg_name))

print 'Trying to save configuration of \'' + evg_name + '\' and ' + str(evrs).strip('[]') + '.'
sys.stdout.flush()

fps=('UNIV0','UNIV1','UNIV2','UNIV3')
no_evr = []
data = {}
data['EVG'] = {'Units' : '','TOE_TE' : ''}

for i in evrs:
	data[i] = {'UNIV0': '', 'UNIV1': '', 'UNIV2': '', 'UNIV3': ''}
	for j in fps:
		data[i][j] = {'Event' : '','Delay' : '','Width' : '','Polarity' : ''}

try:
	# Get PV values
	EVG_te_tot = list(epics.caget("".join((evg,':SoftSeq-1-EvtCode-RB'))))
	EVG_toe_tot = list(epics.caget("".join((evg,':SoftSeq-1-Timestamp-RB'))))
	EVG_units = epics.caget("".join((evg,':SoftSeq-1-TsResolution-RB')), as_string=True)

	max_index = EVG_te_tot.index(127)
	EVG_te0 = EVG_te_tot[0:max_index]
	EVG_te = [int(x) for x in EVG_te0]
	EVG_toe0 = EVG_toe_tot[0:max_index]
	EVG_toe = [float(x) for x in EVG_toe0]	
	
	toe_te = zip(EVG_toe, EVG_te)		

	data['EVG']['TOE_TE'] = dict(toe_te)
	data['EVG']['Units'] = EVG_units
	for i in evrs: # EVR
		pref=''.join((prefix,i))
		check_pv = epics.PV("".join((pref,":Ena-Sel")))
		if (check_pv.status is None):
			print 'Cannot connect to ' + i
			sys.stdout.flush()
			no_evr.append(i)
		else:
			for j in fps: # Front panel 0 - 3
				data[i][j]['Event'] = epics.caget("".join((pref,":Pul",j[-1],"-Evt-Trig0-SP")))
				data[i][j]['Delay'] = epics.caget("".join((pref,":Pul",j[-1],"-Delay-RB")))
				data[i][j]['Width'] = epics.caget("".join((pref,":Pul",j[-1],"-Width-RB")))
				data[i][j]['Polarity'] = epics.caget("".join((pref,":Pul",j[-1],"-Polarity-Sel")))
	
	if (len(no_evr) > 0):
		evrs = [x for x in evrs if x not in no_evr]	
				
	with open(sys.argv[2], 'w') as outfile:
		outfile.write(sys.argv[1])

except Exception:
	with open(sys.argv[2], 'w') as outfile:
		outfile.write('Error')
	raise

with open(sys.argv[1], 'w') as outfile:
	json.dump(data, outfile, sort_keys=True, indent=2)

print 'Configuration of \'' + evg_name + '\' and ' + str(evrs).strip('[]') + ' saved in ' + sys.argv[1] + '.'
print 'Console output written to ' + sys.argv[4]
print 'Done!'

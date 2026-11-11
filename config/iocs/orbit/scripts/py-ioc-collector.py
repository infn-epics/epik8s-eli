import json
import time
import threading
import argparse
import random
import math
import logging
from datetime import datetime
from cothread.catools import camonitor,caget
from softioc import builder, softioc
import numpy as np

class PVCollector:
    def __init__(self, item, driver):
        self.pvname = item['pvname']
        self.coeff = item.get('coeff', None)
        self.off = item.get('off', None)
        self.src = item['src']
        self.update_interval = item['update']
        self.data = [0.0] * len(self.src)
        self.history = [[] for _ in range(len(self.src))]
        self.history_length =driver.hist_len # Default history length
        self.lock = threading.Lock()
        self.driver = driver
        self.rndoff = float(random.uniform(0, 8))
        self.connection_status = [False] * len(self.src)  # Track connection status
        self.connection_errors = []

        self.source_pvs = []
        for i, pv in enumerate(self.src):
            try:
                print(f"* trying to get {pv}...")
                v = caget(pv, timeout=5)
                print(f"* get {pv}={v}")
                self.connection_status[i] = True
            except Exception as e:
                print(f"## cannot connect to {pv}: {e}")
                # Use shorter error message format for EPICS string limit
                error_msg = f"{pv}: {str(e)[:20]}"
                self.connection_errors.append(error_msg)
                self.connection_status[i] = False
                # Set initial data to NaN or invalid value for disconnected PVs
                self.data[i] = float('nan')

        # Only start monitoring for successfully connected PVs
        connected_pvs = [pv for i, pv in enumerate(self.src) if self.connection_status[i]]
        if connected_pvs:
            # Create individual monitors for each connected PV with proper index mapping
            for i, pv_name in enumerate(self.src):
                if self.connection_status[i]:
                    try:
                        camonitor(pv_name, lambda v, idx=i: self.on_value_change_by_index(v, idx))
                    except Exception as e:
                        print(f"Failed to start monitoring {pv_name}: {e}")
        else:
            print(f"## WARNING: No PVs connected for {self.pvname}")
            
        # Start a separate thread to periodically check disconnected PVs
        self.monitor_thread = threading.Thread(target=self.monitor_disconnected_pvs, daemon=True)
        self.monitor_thread.start()

    def format_error_message(self):
        """Format error message for EPICS string record with length limit."""
        if not self.connection_errors:
            return "All connected"
        
        # Try to fit as many errors as possible within the 39 character limit
        if len(self.connection_errors) == 1:
            msg = self.connection_errors[0]
        else:
            # Show count and first error
            first_error = self.connection_errors[0].split(':')[0]  # Just PV name
            msg = f"{len(self.connection_errors)} errors: {first_error}..."
        
        # Ensure we don't exceed EPICS string limit
        if len(msg) > 39:
            msg = msg[:36] + "..."
        
        return msg

    def monitor_disconnected_pvs(self):
        """Periodically check disconnected PVs for reconnection."""
        while True:
            time.sleep(5)  # Check every 5 seconds
            with self.lock:
                for i, pv_name in enumerate(self.src):
                    if not self.connection_status[i]:
                        # Try to reconnect to disconnected PV
                        try:
                            value = caget(pv_name, timeout=1)
                            # If we get here, PV is now connected
                            self.connection_status[i] = True
                            self.data[i] = value
                            # Remove from error list
                            error_patterns = [f"{pv_name}:", f"PV {pv_name}"]
                            self.connection_errors = [err for err in self.connection_errors 
                                                    if not any(pattern in err for pattern in error_patterns)]
                            print(f"PV {pv_name} reconnected")
                            
                            # Start monitoring this PV
                            try:
                                camonitor(pv_name, lambda v, idx=i: self.on_value_change_by_index(v, idx))
                            except Exception as e:
                                print(f"Failed to start monitoring {pv_name}: {e}")
                                
                        except Exception:
                            # Still disconnected, check if error already recorded
                            error_msg = f"{pv_name}: disconnected"
                            if error_msg not in self.connection_errors:
                                self.connection_errors.append(error_msg)
                            continue
                    else:
                        # PV should be connected, verify it still is
                        try:
                            caget(pv_name, timeout=1)
                        except Exception:
                            # PV has disconnected
                            self.connection_status[i] = False
                            self.data[i] = float('nan')
                            error_msg = f"{pv_name}: disconnected"
                            if error_msg not in self.connection_errors:
                                self.connection_errors.append(error_msg)
                            print(f"PV {pv_name} disconnected")

    def on_value_change_by_index(self, value, pv_index):
        """Handle value change for a specific PV index."""
        with self.lock:
            self.data[pv_index] = value
            self.history[pv_index].append(value)
            if len(self.history[pv_index]) > self.history_length:
                self.history[pv_index].pop(0)

    def update_output_pv(self):
        while True:
            with self.lock:
                if self.driver.outmode == 1:
                    combined_value = [float(random.uniform(-5.1, 5.1)) for _ in self.src]
                elif self.driver.outmode == 2:
                    fas = float(random.uniform(0, 360))
                    combined_value = [(self.rndoff * 2) * (math.sin(math.radians(20 * i + fas))) for i in range(len(self.src))]
                else:
                    combined_value = self.data.copy()
                
                if self.coeff:
                    if isinstance(self.coeff, list):
                        combined_value = [a * b for a, b in zip(combined_value, self.coeff)]
                    else:
                        combined_value = [x * self.coeff for x in combined_value]

                if self.off:
                    if isinstance(self.off, list):
                        combined_value = [a + b for a, b in zip(combined_value, self.off)]
                    else:
                        combined_value = [a + self.off for a in combined_value]
                
                # Calculate averages and standard deviations
                avg_values = [np.mean(hist) if hist else 0.0 for hist in self.history]
                std_values = [np.std(hist) if hist else 0.0 for hist in self.history]

                # Update the PVs
                # Handle NaN values by replacing with 0.0 for output
                output_values = [val if not np.isnan(val) else 0.0 for val in combined_value]
                self.driver.out[self.pvname].set(output_values)
                self.driver.out[f'{self.pvname}_avg'].set(avg_values)
                self.driver.out[f'{self.pvname}_std'].set(std_values)
                
                # Update connection status waveform
                if f'{self.pvname}_CONN' in self.driver.out:
                    conn_status = [1 if status else 0 for status in self.connection_status]
                    self.driver.out[f'{self.pvname}_CONN'].set(conn_status)
                
                # Update alarm status
                if f'{self.pvname}_ALARM' in self.driver.out:
                    disconnected_count = sum(1 for status in self.connection_status if not status)
                    total_count = len(self.connection_status)
                    
                    if disconnected_count == total_count:
                        alarm_severity = 3  # INVALID - all disconnected
                    elif disconnected_count > 0:
                        alarm_severity = 2  # MAJOR - some disconnected
                    else:
                        alarm_severity = 0  # OK - all connected
                    
                    self.driver.out[f'{self.pvname}_ALARM'].set(alarm_severity)
                
                # Update error message
                if f'{self.pvname}_ERROR' in self.driver.out:
                    error_msg = self.format_error_message()
                    self.driver.out[f'{self.pvname}_ERROR'].set(error_msg)

            time.sleep(self.update_interval / 1000.0)

class MyDriver:
    def __init__(self, config):
        self.collectors = {}
        self.out = {}
        self.outmode = 0
        self.hist_len=config.get('history', 10) 
        prefix = config.get('prefix')
        
            
        builder.SetDeviceName(prefix)
        builder.mbbOut("CMD", ('HW', 0), ('RNDSIM', 1), ('SINSIM', 2), on_update=self.handle_cmd, initial_value=self.outmode)

        for item in config.get('collect', []):
            if 'src' in item:
                input_collector = PVCollector(item, self)
                self.collectors[item['pvname']] = input_collector
                print(f"Initializing {item['pvname']} as array {len(item['src'])}")
                pvout = builder.WaveformIn(item['pvname'], initial_value=[0.0] * len(item['src']),length=len(item['src']))
                self.out[item['pvname']] = pvout
                # Create PVs for average and standard deviation
                pvout_avg = builder.WaveformIn(f'{item["pvname"]}_avg', initial_value=[0.0] * len(item['src']),length=len(item['src']))
                pvout_std = builder.WaveformIn(f'{item["pvname"]}_std', initial_value=[0.0] * len(item['src']),length=len(item['src']))
                self.out[f'{item["pvname"]}_avg'] = pvout_avg
                self.out[f'{item["pvname"]}_std'] = pvout_std
                
                # Create connection status PV
                conn_status = [1 if status else 0 for status in input_collector.connection_status]
                pvout_conn = builder.WaveformIn(f'{item["pvname"]}_CONN', initial_value=conn_status, length=len(item['src']))
                self.out[f'{item["pvname"]}_CONN'] = pvout_conn
                
                # Create alarm status PV (0=OK, 1=MINOR, 2=MAJOR, 3=INVALID)
                disconnected_count = sum(1 for status in input_collector.connection_status if not status)
                if disconnected_count == len(item['src']):
                    alarm_severity = 3  # INVALID - all disconnected
                elif disconnected_count > 0:
                    alarm_severity = 2  # MAJOR - some disconnected
                else:
                    alarm_severity = 0  # OK - all connected
                    
                pvout_alarm = builder.aIn(f'{item["pvname"]}_ALARM', initial_value=alarm_severity)
                self.out[f'{item["pvname"]}_ALARM'] = pvout_alarm
                
                # Create error message PV
                error_msg = input_collector.format_error_message()
                pvout_error = builder.stringIn(f'{item["pvname"]}_ERROR', initial_value=error_msg)
                self.out[f'{item["pvname"]}_ERROR'] = pvout_error
            if 'const' in item:
                input_consts = item['const']
                pvout = builder.WaveformIn(item['pvname'], initial_value=input_consts)
                self.out[item['pvname']] = pvout

        # Create an 'ao' record to configure the history length
        self.history_length_pv = builder.aOut('HIST', initial_value=10, on_update=self.update_history_length)

    def update_history_length(self, value=None, **kwargs):
        for collector in self.collectors.values():
            collector.history_length = int(value)
        logging.info(f"Updated history length to {value}")

    def handle_cmd(self, value=None, **kwargs):
        self.outmode = value
        logging.info(f"Mode {value}")

    def _start_threads(self):
        for collector in self.collectors:
            threading.Thread(target=self.collectors[collector].update_output_pv, name=collector, daemon=True).start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, default="config.json", help="The configuration name")
    parser.add_argument("-p", "--pvout", required=False, default="pvlist.txt", help="Output PVlist")

    args = parser.parse_args()
    
    print(f"* Opening {args.conf}")
    with open(args.conf, 'r') as f:
        config = json.load(f)
    
    print(f"* Create prefix {config.get('prefix')}")
    driver = MyDriver(config)

    builder.LoadDatabase()
    softioc.iocInit()
    driver._start_threads()

    import os
    softioc.dbl()

    with open(args.pvout, "w") as f:
        old_stdout = os.dup(1)
        os.dup2(f.fileno(), 1)
        softioc.dbl()
        os.dup2(old_stdout, 1)
        os.close(old_stdout)

    softioc.interactive_ioc(globals())

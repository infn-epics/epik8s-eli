<?xml version="1.0" encoding="UTF-8"?>
<databrowser>
  <title>ICT Charge Trend - Channel 0</title>
  <show_toolbar>true</show_toolbar>
  <update_period>1.0</update_period>
  <scroll_step>5</scroll_step>
  <time_range>1 hour</time_range>
  <background>
    <red>255</red>
    <green>255</green>
    <blue>255</blue>
  </background>
  <annotations />
  <pvlist>
    <pv>
      <display_name>Calculated Charge Trend</display_name>
      <visible>true</visible>
      <name>$(DEVICE):AI$(CHAN):CHARGE_FINAL</name>
      <axis>0</axis>
      <color>
        <red>0</red>
        <green>0</green>
        <blue>255</blue>
      </color>
      <trace_type>SINGLE_LINE</trace_type>
      <linewidth>2</linewidth>
      <line_style>SOLID</line_style>
      <point_type>NONE</point_type>
      <point_size>2</point_size>
      <waveform_index>0</waveform_index>
      <period>0.5</period>
      <ring_size>20000</ring_size>
      <request>RAW</request>
      <archive>
        <name>pbraw://da-test-archiver.k8sda.lnf.infn.it/retrieval</name>
        <url>pbraw://da-test-archiver.k8sda.lnf.infn.it/retrieval</url>
        <key>1</key>
      </archive>	
     </pv>
  </pvlist>
  <axes>
    <axis>
      <visible>true</visible>
      <name>Charge [pC]</name>
      <use_axis_name>true</use_axis_name>
      <use_trace_names>false</use_trace_names>
      <right>false</right>
      <color>
        <red>0</red>
        <green>0</green>
        <blue>0</blue>
      </color>
      <min>0.0</min>
      <max>50.0</max>
      <grid>true</grid>
      <autoscale>true</autoscale>
      <log_scale>false</log_scale>
    </axis>
  </axes>
</databrowser>
<?xml version="1.0" encoding="UTF-8"?>
<!--Phoebus Data Browser plot for LLRF01 RF Power and Control-->
<databrowser>
  <title>LLRF01 - RF Power &amp; Control</title>
  <show_toolbar>true</show_toolbar>
  <update_period>1.0</update_period>
  <scroll_step>5</scroll_step>
  <scroll>true</scroll>
  <start>-1 hours</start>
  <end>now</end>
  <archive_rescale>STAGGER</archive_rescale>
  <foreground>
    <red>0</red>
    <green>0</green>
    <blue>0</blue>
  </foreground>
  <background>
    <red>255</red>
    <green>255</green>
    <blue>255</blue>
  </background>
  <title_font>Liberation Sans|20|1</title_font>
  <label_font>Liberation Sans|14|1</label_font>
  <scale_font>Liberation Sans|12|0</scale_font>
  <legend_font>Liberation Sans|12|0</legend_font>
  <axes>
    <axis>
      <visible>true</visible>
      <name>Power (W)</name>
      <use_axis_name>true</use_axis_name>
      <use_trace_names>true</use_trace_names>
      <right>false</right>
      <color>
        <red>0</red>
        <green>0</green>
        <blue>0</blue>
      </color>
      <min>0.0</min>
      <max>1.0E7</max>
      <grid>true</grid>
      <autoscale>true</autoscale>
      <log_scale>false</log_scale>
    </axis>
    <axis>
      <visible>true</visible>
      <name>Phase (deg)</name>
      <use_axis_name>true</use_axis_name>
      <use_trace_names>true</use_trace_names>
      <right>true</right>
      <color>
        <red>128</red>
        <green>0</green>
        <blue>128</blue>
      </color>
      <min>-180.0</min>
      <max>180.0</max>
      <grid>false</grid>
      <autoscale>true</autoscale>
      <log_scale>false</log_scale>
    </axis>
  </axes>
  <annotations>
  </annotations>
  <pvlist>
    <!-- Setpoint Power -->
    <pv>
      <display_name>SP Power</display_name>
      <visible>true</visible>
      <name>LEL-RF-LLRF01:vm:dsp:sp_amp:power</name>
      <axis>0</axis>
      <color>
        <red>0</red>
        <green>0</green>
        <blue>255</blue>
      </color>
      <trace_type>AREA</trace_type>
      <linewidth>2</linewidth>
      <line_style>SOLID</line_style>
      <point_type>NONE</point_type>
      <point_size>2</point_size>
      <waveform_index>0</waveform_index>
      <period>0.0</period>
      <ring_size>5000</ring_size>
      <request>OPTIMIZED</request>
      <archive>
        <name>eli-archiver</name>
        <url>pbraw://eli-archiver.srv.int.eli-np.ro/retrieval</url>
        <key>1</key>
      </archive>
    </pv>
    <!-- Feedforward Power -->
    <pv>
      <display_name>FF Power</display_name>
      <visible>true</visible>
      <name>LEL-RF-LLRF01:vm:dsp:ff_amp:power</name>
      <axis>0</axis>
      <color>
        <red>0</red>
        <green>128</green>
        <blue>0</blue>
      </color>
      <trace_type>SINGLE_LINE</trace_type>
      <linewidth>2</linewidth>
      <line_style>SOLID</line_style>
      <point_type>NONE</point_type>
      <point_size>2</point_size>
      <waveform_index>0</waveform_index>
      <period>0.0</period>
      <ring_size>5000</ring_size>
      <request>OPTIMIZED</request>
      <archive>
        <name>eli-archiver</name>
        <url>pbraw://eli-archiver.srv.int.eli-np.ro/retrieval</url>
        <key>1</key>
      </archive>
    </pv>
    <!-- Setpoint Phase -->
    <pv>
      <display_name>SP Phase</display_name>
      <visible>true</visible>
      <name>LEL-RF-LLRF01:vm:dsp:sp_ph:phase</name>
      <axis>1</axis>
      <color>
        <red>255</red>
        <green>0</green>
        <blue>255</blue>
      </color>
      <trace_type>SINGLE_LINE</trace_type>
      <linewidth>2</linewidth>
      <line_style>DASH</line_style>
      <point_type>NONE</point_type>
      <point_size>2</point_size>
      <waveform_index>0</waveform_index>
      <period>0.0</period>
      <ring_size>5000</ring_size>
      <request>OPTIMIZED</request>
      <archive>
        <name>eli-archiver</name>
        <url>pbraw://eli-archiver.srv.int.eli-np.ro/retrieval</url>
        <key>1</key>
      </archive>
    </pv>
    <!-- Feedforward Phase -->
    <pv>
      <display_name>FF Phase</display_name>
      <visible>true</visible>
      <name>LEL-RF-LLRF01:vm:dsp:ff_ph:phase</name>
      <axis>1</axis>
      <color>
        <red>128</red>
        <green>0</green>
        <blue>128</blue>
      </color>
      <trace_type>SINGLE_LINE</trace_type>
      <linewidth>2</linewidth>
      <line_style>SOLID</line_style>
      <point_type>NONE</point_type>
      <point_size>2</point_size>
      <waveform_index>0</waveform_index>
      <period>0.0</period>
      <ring_size>5000</ring_size>
      <request>OPTIMIZED</request>
      <archive>
        <name>eli-archiver</name>
        <url>pbraw://eli-archiver.srv.int.eli-np.ro/retrieval</url>
        <key>1</key>
      </archive>
    </pv>
  </pvlist>
</databrowser>

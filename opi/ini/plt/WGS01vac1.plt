<?xml version="1.0" encoding="UTF-8"?>
<databrowser>
  <title>WGS01 Vacuum (Clean)</title>

  <show_toolbar>true</show_toolbar>
  <update_period>3.0</update_period>
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

  <!-- Fonts -->
  <title_font>Liberation Sans|20|1</title_font>
  <label_font>Liberation Sans|10|1</label_font>
  <scale_font>Liberation Sans|14|0</scale_font>
  <legend_font>Liberation Sans|12|0</legend_font>

  <!-- Axis -->
  <axes>
    <axis>
      <visible>true</visible>
      <name>Pressure [mbar]</name>
      <use_axis_name>false</use_axis_name>
      <use_trace_names>true</use_trace_names>
      <right>false</right>

      <color>
        <red>0</red>
        <green>0</green>
        <blue>0</blue>
      </color>

      <!-- Adjusted range for better readability -->
      <min>1.0E-9</min>
      <max>5.0E-8</max>

      <grid>true</grid>
      <autoscale>true</autoscale>
      <log_scale>true</log_scale>
    </axis>
  </axes>

  <annotations>
  </annotations>

  <pvlist>

    <!-- PV 1 -->
    <pv>
      <display_name>WGS01IONP01</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON04:WGS01IONP01:PRES_RB</name>
      <axis>0</axis>
      <color><red>155</red><green>0</green><blue>0</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

    <!-- PV 2 -->
    <pv>
      <display_name>WGS01IONP02</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON04:WGS01IONP02:PRES_RB</name>
      <axis>0</axis>
      <color><red>0</red><green>180</green><blue>0</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

    <!-- PV 3 -->
    <pv>
      <display_name>WGS01IONP03</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON04:WGS01IONP03:PRES_RB</name>
      <axis>0</axis>
      <color><red>0</red><green>0</green><blue>255</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

    <!-- PV 4 -->
    <pv>
      <display_name>WGS01IONP04</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON04:WGS01IONP04:PRES_RB</name>
      <axis>0</axis>
      <color><red>255</red><green>127</green><blue>0</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

    <!-- PV 5 -->
    <pv>
      <display_name>WGS01IONP05</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON05:WGS01IONP05:PRES_RB</name>
      <axis>0</axis>
      <color><red>191</red><green>55</green><blue>110</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

    <!-- PV 6 -->
    <pv>
      <display_name>WGS01IONP06</display_name>
      <visible>true</visible>
      <name>LEL:VAC:VPCON05:WGS01IONP06:PRES_RB</name>
      <axis>0</axis>
      <color><red>0</red><green>200</green><blue>200</blue></color>
      <trace_type>LINE</trace_type>
      <linewidth>2</linewidth>
    </pv>

  </pvlist>
</databrowser>
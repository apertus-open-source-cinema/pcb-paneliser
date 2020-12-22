<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="7.7.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="yes" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="16" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="17" fill="1" visible="no" active="no"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="no"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="no"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="no"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="no"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="no"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="no"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="no"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="no"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="no"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="no"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="no"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="no"/>
<layer number="15" name="Route15" color="18" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="19" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="sma">
<packages>
<package name="SMA-EDGE">
<wire x1="0" y1="3.2" x2="1.6" y2="3.2" width="0.2032" layer="51"/>
<wire x1="1.6" y1="3.2" x2="1.6" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="1.6" y1="-3.2" x2="0" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="0" y1="-3.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<smd name="1" x="-2.3" y="0" dx="4.6" dy="1.73" layer="1"/>
<smd name="2@4" x="-2.3" y="2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<smd name="2@3" x="-2.3" y="-2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<text x="-2.54" y="4.445" size="1.27" layer="25">&gt;NAME</text>
<text x="-3.175" y="-5.715" size="1.27" layer="27">&gt;VALUE</text>
<wire x1="0" y1="-2.2" x2="0" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="0.4" x2="0" y2="2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="1.8" y1="2.9" x2="4.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="2.9" x2="4.5" y2="3.1" width="0.2032" layer="21"/>
<wire x1="8.1" y1="3.1" x2="8.4" y2="2.9" width="0.2032" layer="21"/>
<wire x1="8.4" y1="2.9" x2="8.7" y2="2.9" width="0.2032" layer="21"/>
<wire x1="8.7" y1="2.9" x2="9.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="9.6" y1="-2.9" x2="9.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.5" y1="3.1" x2="4.8" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.8" y1="2.9" x2="5.1" y2="3.1" width="0.2032" layer="21"/>
<wire x1="5.1" y1="3.1" x2="5.4" y2="2.9" width="0.2032" layer="21"/>
<wire x1="5.4" y1="2.9" x2="5.7" y2="3.1" width="0.2032" layer="21"/>
<wire x1="5.7" y1="3.1" x2="6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="6" y1="2.9" x2="6.3" y2="3.1" width="0.2032" layer="21"/>
<wire x1="6.3" y1="3.1" x2="6.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="6.6" y1="2.9" x2="6.9" y2="3.1" width="0.2032" layer="21"/>
<wire x1="6.9" y1="3.1" x2="7.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="7.2" y1="2.9" x2="7.5" y2="3.1" width="0.2032" layer="21"/>
<wire x1="7.5" y1="3.1" x2="7.8" y2="2.9" width="0.2032" layer="21"/>
<wire x1="7.8" y1="2.9" x2="8.1" y2="3.1" width="0.2032" layer="21"/>
<wire x1="1.8" y1="-2.9" x2="4.2" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="-2.9" x2="4.5" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.5" y1="-2.9" x2="4.8" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="8.4" y1="-3.1" x2="8.7" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="8.7" y1="-2.9" x2="9.6" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.8" y1="-3.1" x2="5.1" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="5.1" y1="-2.9" x2="5.4" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="5.4" y1="-3.1" x2="5.7" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="5.7" y1="-2.9" x2="6" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="6" y1="-3.1" x2="6.3" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="6.3" y1="-2.9" x2="6.6" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="6.6" y1="-3.1" x2="6.9" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="6.9" y1="-2.9" x2="7.2" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="7.2" y1="-3.1" x2="7.5" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="7.5" y1="-2.9" x2="7.8" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="7.8" y1="-3.1" x2="8.1" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="8.1" y1="-2.9" x2="8.4" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="8.7" y1="-2.9" x2="8.7" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="-2.9" x2="4.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="-4" y1="3.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="-4" y2="2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="2.2" x2="-4" y2="3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-2.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="-3.2" x2="-4" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-3.2" x2="-4" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="-4" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="-4" y1="-0.4" x2="-4" y2="0.4" width="0.2032" layer="51"/>
</package>
<package name="SMA_EDGE_2SIDE">
<wire x1="0" y1="3.2" x2="1.6" y2="3.2" width="0.2032" layer="51"/>
<wire x1="1.6" y1="3.2" x2="1.6" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="1.6" y1="-3.2" x2="0" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="0" y1="-3.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<smd name="1" x="-2.3" y="0" dx="4.6" dy="1.73" layer="1"/>
<smd name="2@4" x="-2.3" y="2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<smd name="2@3" x="-2.3" y="-2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<text x="-2.54" y="4.445" size="1.27" layer="25">&gt;NAME</text>
<text x="-3.175" y="-5.715" size="1.27" layer="27">&gt;VALUE</text>
<wire x1="0" y1="-2.2" x2="0" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="0.4" x2="0" y2="2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="1.8" y1="2.9" x2="4.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="2.9" x2="4.5" y2="3.1" width="0.2032" layer="21"/>
<wire x1="8.1" y1="3.1" x2="8.4" y2="2.9" width="0.2032" layer="21"/>
<wire x1="8.4" y1="2.9" x2="8.7" y2="2.9" width="0.2032" layer="21"/>
<wire x1="8.7" y1="2.9" x2="9.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="9.6" y1="-2.9" x2="9.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.5" y1="3.1" x2="4.8" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.8" y1="2.9" x2="5.1" y2="3.1" width="0.2032" layer="21"/>
<wire x1="5.1" y1="3.1" x2="5.4" y2="2.9" width="0.2032" layer="21"/>
<wire x1="5.4" y1="2.9" x2="5.7" y2="3.1" width="0.2032" layer="21"/>
<wire x1="5.7" y1="3.1" x2="6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="6" y1="2.9" x2="6.3" y2="3.1" width="0.2032" layer="21"/>
<wire x1="6.3" y1="3.1" x2="6.6" y2="2.9" width="0.2032" layer="21"/>
<wire x1="6.6" y1="2.9" x2="6.9" y2="3.1" width="0.2032" layer="21"/>
<wire x1="6.9" y1="3.1" x2="7.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="7.2" y1="2.9" x2="7.5" y2="3.1" width="0.2032" layer="21"/>
<wire x1="7.5" y1="3.1" x2="7.8" y2="2.9" width="0.2032" layer="21"/>
<wire x1="7.8" y1="2.9" x2="8.1" y2="3.1" width="0.2032" layer="21"/>
<wire x1="1.8" y1="-2.9" x2="4.2" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="-2.9" x2="4.5" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.5" y1="-2.9" x2="4.8" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="8.4" y1="-3.1" x2="8.7" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="8.7" y1="-2.9" x2="9.6" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="4.8" y1="-3.1" x2="5.1" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="5.1" y1="-2.9" x2="5.4" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="5.4" y1="-3.1" x2="5.7" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="5.7" y1="-2.9" x2="6" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="6" y1="-3.1" x2="6.3" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="6.3" y1="-2.9" x2="6.6" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="6.6" y1="-3.1" x2="6.9" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="6.9" y1="-2.9" x2="7.2" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="7.2" y1="-3.1" x2="7.5" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="7.5" y1="-2.9" x2="7.8" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="7.8" y1="-3.1" x2="8.1" y2="-2.9" width="0.2032" layer="21"/>
<wire x1="8.1" y1="-2.9" x2="8.4" y2="-3.1" width="0.2032" layer="21"/>
<wire x1="8.7" y1="-2.9" x2="8.7" y2="2.9" width="0.2032" layer="21"/>
<wire x1="4.2" y1="-2.9" x2="4.2" y2="2.9" width="0.2032" layer="21"/>
<wire x1="-4" y1="3.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="-4" y2="2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="2.2" x2="-4" y2="3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-2.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="-3.2" x2="-4" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-3.2" x2="-4" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="-4" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="-4" y1="-0.4" x2="-4" y2="0.4" width="0.2032" layer="51"/>
<smd name="2@1" x="-2.3" y="2.6" dx="4.6" dy="1.9" layer="16" rot="R180"/>
<smd name="2@2" x="-2.3" y="-2.6" dx="4.6" dy="1.9" layer="16" rot="R180"/>
</package>
<package name="SMA-EDGE_ND">
<wire x1="0" y1="-3.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<smd name="1" x="-2.3" y="0" dx="4.6" dy="1.73" layer="1"/>
<smd name="2@4" x="-2.3" y="2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<smd name="2@3" x="-2.3" y="-2.6" dx="4.6" dy="1.9" layer="1" rot="R180"/>
<text x="-2.54" y="4.445" size="1.27" layer="25">&gt;NAME</text>
<text x="-3.175" y="-5.715" size="1.27" layer="27">&gt;VALUE</text>
<wire x1="0" y1="-2.2" x2="0" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="0.4" x2="0" y2="2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="3.2" x2="0" y2="3.2" width="0.2032" layer="51"/>
<wire x1="0" y1="2.2" x2="-4" y2="2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="2.2" x2="-4" y2="3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-2.2" x2="0" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="0" y1="-3.2" x2="-4" y2="-3.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="-3.2" x2="-4" y2="-2.2" width="0.2032" layer="51"/>
<wire x1="-4" y1="0.4" x2="0" y2="0.4" width="0.2032" layer="51"/>
<wire x1="0" y1="-0.4" x2="-4" y2="-0.4" width="0.2032" layer="51"/>
<wire x1="-4" y1="-0.4" x2="-4" y2="0.4" width="0.2032" layer="51"/>
</package>
</packages>
<symbols>
<symbol name="BNC-FGND">
<wire x1="0" y1="-2.54" x2="-0.762" y2="-1.778" width="0.254" layer="94"/>
<wire x1="0" y1="0" x2="-0.508" y2="0" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="0.508" x2="-0.762" y2="0.508" width="0.254" layer="94"/>
<wire x1="-0.762" y1="0.508" x2="-0.508" y2="0" width="0.254" layer="94"/>
<wire x1="-0.508" y1="0" x2="-0.762" y2="-0.508" width="0.254" layer="94"/>
<wire x1="-0.762" y1="-0.508" x2="-2.54" y2="-0.508" width="0.254" layer="94"/>
<wire x1="-2.54" y1="2.54" x2="0" y2="0.508" width="0.3048" layer="94" curve="-79.611142" cap="flat"/>
<wire x1="-2.54" y1="-2.54" x2="0" y2="-0.508" width="0.3048" layer="94" curve="79.611142" cap="flat"/>
<text x="-2.54" y="-5.08" size="1.778" layer="96">&gt;VALUE</text>
<text x="-2.54" y="3.302" size="1.778" layer="95">&gt;NAME</text>
<pin name="1" x="2.54" y="0" visible="off" length="short" direction="pas" rot="R180"/>
<pin name="2" x="2.54" y="-2.54" visible="off" length="short" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="BU-SMA-E">
<gates>
<gate name="A" symbol="BNC-FGND" x="0" y="0"/>
</gates>
<devices>
<device name="" package="SMA-EDGE">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2@3 2@4"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="-2SIDE" package="SMA_EDGE_2SIDE">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2@1 2@2 2@3 2@4"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="-ND" package="SMA-EDGE_ND">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2@3 2@4"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="supply1">
<description>&lt;b&gt;Supply Symbols&lt;/b&gt;&lt;p&gt;
 GND, VCC, 0V, +5V, -5V, etc.&lt;p&gt;
 Please keep in mind, that these devices are necessary for the
 automatic wiring of the supply signals.&lt;p&gt;
 The pin name defined in the symbol is identical to the net which is to be wired automatically.&lt;p&gt;
 In this library the device names are the same as the pin names of the symbols, therefore the correct signal names appear next to the supply symbols in the schematic.&lt;p&gt;
 &lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="GND">
<wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.254" layer="94"/>
<text x="-2.54" y="-2.54" size="1.778" layer="96">&gt;VALUE</text>
<pin name="GND" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="GND" prefix="GND">
<description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt;</description>
<gates>
<gate name="1" symbol="GND" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0.1524" drill="0.2032">
<clearance class="0" value="0.1524"/>
</class>
<class number="1" name="LVDS" width="0.1524" drill="0.2032">
<clearance class="1" value="0.1524"/>
</class>
</classes>
<parts>
<part name="X1" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="X2" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="GND7" library="supply1" deviceset="GND" device=""/>
<part name="X3" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="X4" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="GND8" library="supply1" deviceset="GND" device=""/>
<part name="X5" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="X6" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="GND1" library="supply1" deviceset="GND" device=""/>
<part name="X7" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="X8" library="sma" deviceset="BU-SMA-E" device="-ND" value="BU-SMA-E-ND"/>
<part name="GND2" library="supply1" deviceset="GND" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="X1" gate="A" x="27.94" y="48.26" smashed="yes">
<attribute name="NAME" x="25.4" y="51.562" size="1.778" layer="95"/>
</instance>
<instance part="X2" gate="A" x="27.94" y="38.1" smashed="yes">
<attribute name="NAME" x="25.4" y="41.402" size="1.778" layer="95"/>
</instance>
<instance part="GND7" gate="1" x="33.02" y="27.94"/>
<instance part="X3" gate="A" x="99.06" y="48.26" smashed="yes" rot="MR0">
<attribute name="NAME" x="101.6" y="51.562" size="1.778" layer="95" rot="MR0"/>
</instance>
<instance part="X4" gate="A" x="99.06" y="38.1" smashed="yes" rot="MR0">
<attribute name="NAME" x="101.6" y="41.402" size="1.778" layer="95" rot="MR0"/>
</instance>
<instance part="GND8" gate="1" x="93.98" y="27.94" rot="MR0"/>
<instance part="X5" gate="A" x="27.94" y="-22.86" smashed="yes">
<attribute name="NAME" x="25.4" y="-19.558" size="1.778" layer="95"/>
</instance>
<instance part="X6" gate="A" x="27.94" y="-33.02" smashed="yes">
<attribute name="NAME" x="25.4" y="-29.718" size="1.778" layer="95"/>
</instance>
<instance part="GND1" gate="1" x="33.02" y="-43.18"/>
<instance part="X7" gate="A" x="99.06" y="-22.86" smashed="yes" rot="MR0">
<attribute name="NAME" x="101.6" y="-19.558" size="1.778" layer="95" rot="MR0"/>
</instance>
<instance part="X8" gate="A" x="99.06" y="-33.02" smashed="yes" rot="MR0">
<attribute name="NAME" x="101.6" y="-29.718" size="1.778" layer="95" rot="MR0"/>
</instance>
<instance part="GND2" gate="1" x="93.98" y="-43.18" rot="MR0"/>
</instances>
<busses>
</busses>
<nets>
<net name="GND" class="0">
<segment>
<pinref part="X1" gate="A" pin="2"/>
<wire x1="30.48" y1="45.72" x2="33.02" y2="45.72" width="0.1524" layer="91"/>
<pinref part="X2" gate="A" pin="2"/>
<wire x1="30.48" y1="35.56" x2="33.02" y2="35.56" width="0.1524" layer="91"/>
<wire x1="33.02" y1="45.72" x2="33.02" y2="35.56" width="0.1524" layer="91"/>
<wire x1="33.02" y1="35.56" x2="33.02" y2="30.48" width="0.1524" layer="91"/>
<junction x="33.02" y="35.56"/>
<pinref part="GND7" gate="1" pin="GND"/>
</segment>
<segment>
<pinref part="X3" gate="A" pin="2"/>
<wire x1="96.52" y1="45.72" x2="93.98" y2="45.72" width="0.1524" layer="91"/>
<pinref part="X4" gate="A" pin="2"/>
<wire x1="96.52" y1="35.56" x2="93.98" y2="35.56" width="0.1524" layer="91"/>
<wire x1="93.98" y1="45.72" x2="93.98" y2="35.56" width="0.1524" layer="91"/>
<wire x1="93.98" y1="35.56" x2="93.98" y2="30.48" width="0.1524" layer="91"/>
<junction x="93.98" y="35.56"/>
<pinref part="GND8" gate="1" pin="GND"/>
</segment>
<segment>
<pinref part="X5" gate="A" pin="2"/>
<wire x1="30.48" y1="-25.4" x2="33.02" y2="-25.4" width="0.1524" layer="91"/>
<pinref part="X6" gate="A" pin="2"/>
<wire x1="30.48" y1="-35.56" x2="33.02" y2="-35.56" width="0.1524" layer="91"/>
<wire x1="33.02" y1="-25.4" x2="33.02" y2="-35.56" width="0.1524" layer="91"/>
<wire x1="33.02" y1="-35.56" x2="33.02" y2="-40.64" width="0.1524" layer="91"/>
<junction x="33.02" y="-35.56"/>
<pinref part="GND1" gate="1" pin="GND"/>
</segment>
<segment>
<pinref part="X7" gate="A" pin="2"/>
<wire x1="96.52" y1="-25.4" x2="93.98" y2="-25.4" width="0.1524" layer="91"/>
<pinref part="X8" gate="A" pin="2"/>
<wire x1="96.52" y1="-35.56" x2="93.98" y2="-35.56" width="0.1524" layer="91"/>
<wire x1="93.98" y1="-25.4" x2="93.98" y2="-35.56" width="0.1524" layer="91"/>
<wire x1="93.98" y1="-35.56" x2="93.98" y2="-40.64" width="0.1524" layer="91"/>
<junction x="93.98" y="-35.56"/>
<pinref part="GND2" gate="1" pin="GND"/>
</segment>
</net>
<net name="SIGA_P" class="1">
<segment>
<pinref part="X1" gate="A" pin="1"/>
<wire x1="30.48" y1="48.26" x2="96.52" y2="48.26" width="0.1524" layer="91"/>
<pinref part="X3" gate="A" pin="1"/>
</segment>
</net>
<net name="SIGA_N" class="1">
<segment>
<pinref part="X2" gate="A" pin="1"/>
<wire x1="30.48" y1="38.1" x2="96.52" y2="38.1" width="0.1524" layer="91"/>
<pinref part="X4" gate="A" pin="1"/>
</segment>
</net>
<net name="SIGB_P" class="0">
<segment>
<pinref part="X5" gate="A" pin="1"/>
<wire x1="30.48" y1="-22.86" x2="96.52" y2="-22.86" width="0.1524" layer="91"/>
<pinref part="X7" gate="A" pin="1"/>
</segment>
</net>
<net name="SIGB_N" class="0">
<segment>
<pinref part="X6" gate="A" pin="1"/>
<wire x1="30.48" y1="-33.02" x2="96.52" y2="-33.02" width="0.1524" layer="91"/>
<pinref part="X8" gate="A" pin="1"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>

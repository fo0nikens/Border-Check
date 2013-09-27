#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
BC (Border-Check) is a tool to retrieve info of traceroute tests over website navigation routes.
GPLv3 - 2013 by psy (epsylon@riseup.net)
"""
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

  # extract data from a xml file
f = open('data.xml', 'r')
f2 = open('data.xml', 'r')
xml = ET.parse(f)
data = f2.read()
dom = parseString(data.encode('utf-8'))
f.close()
f2.close()
n_hops = dom.getElementsByTagName('hop')[-1].toxml().replace('<hop>', '').replace('</hop','')
hop_list = []
hop_ip_list =[]
geoarray = []
latlong= []
asn_list =[]
server_name_list = []
timestamp_list = []
last_hop = int(xml.findall('hop')[-1].text)
country_code_list = []

for counter in range(0, last_hop+1):
    url = xml.getroot().text
    hop_element = parseString(dom.getElementsByTagName('hop')[counter].toxml().encode('utf-8'))
    hop = xml.findall('hop')[counter].text
    server_name = hop_element.getElementsByTagName('server_name')[0].toxml().replace('<server_name>','').replace('</server_name>','')
    asn = hop_element.getElementsByTagName('asn')[0].toxml().replace('<asn>','').replace('</asn>','')
    hop_ip = hop_element.getElementsByTagName('hop_ip')[0].toxml().replace('<hop_ip>','').replace('</hop_ip>','')
    longitude = hop_element.getElementsByTagName('longitude')[0].toxml().replace('<longitude>','').replace('</longitude>','')
    latitude = hop_element.getElementsByTagName('latitude')[0].toxml().replace('<latitude>','').replace('</latitude>','')
    timestamp = hop_element.getElementsByTagName('timestamp')[0].toxml().replace('<timestamp>','').replace('</timestamp>','')
    country_code = hop_element.getElementsByTagName('country_code')[0].toxml().replace('<country_code>','').replace('</country_code>','')

    latlong = [float(latitude.encode('utf-8')), float(longitude.encode('utf-8'))]
    geoarray.append(latlong)
    asn_list.append(asn.encode('utf-8'))
    hop = int(hop) +1
    hop_list.append(str(hop))
    hop_ip_list.append(hop_ip.encode('utf-8'))
    server_name_list.append(server_name.encode('utf-8'))
    timestamp_list.append(float(timestamp))
    country_code_list.append(country_code.encode('utf-8'))

unique_country_code_list = set(country_code_list)


# HTML + JS container
output = """
<html>
<head>
  <title>Border Check - Web Viewer</title>
  <link rel="stylesheet" href="js/leaflet/leaflet.css" />
  <link rel="stylesheet" href="style.css" />
  <link rel="stylesheet" href="js/cluster/MarkerCluster.Default.css"/>
  <link rel="stylesheet" href="js/cluster/MarkerCluster.css"/>
  <script src="js/leaflet/leaflet.js"></script>
  <script src="js/jquery-1.10.2.min.js"></script>
  <script src="js/rlayer-src.js"></script>
  <script src="js/raphael.js"></script>
  <script src="js/bc.js"></script>
  <script src="js/favicon.js"></script>
  <script src="js/cluster/leaflet.markercluster-src.js"></script>


  <script type="text/javascript">
        $(document).ready (function(){
          var h = $(window).innerHeight();
          var w = $(window).innerWidth();
          $("#wrapper").css({
            "width": w, "height": h
            })
          })
  </script>
</head>
<body>
  <div id="wrapper">
      <div class="header">Travelling to:</div>
      <div class ="header" id="url">"""+url+"""</div>
      <div id="map" style="width: 100%; height: 100%"></div>
      <div class ="bar">
      <div id="button" class='toggle'> > </div>
      <div class = info>
      <div> <img src='images/bclogo.png'></img></div>
      <div id='info-text'>
      <br /><div class='toggle' id='about'>About</div>
      <div id='about-content'>
      <p>As you surf the net, data packets are sent from your computer to the target server. These data packets go on a journey hopping from server to server, potentially crossing multiple countries and networks, until the packets reach the desired website.</p>
      <p> Border Check allows you to retrace the path your data takes across the internet's infrastructure. It will map out all the servers your data passes and shows you in which countries or cities these servers are located. Additionally Border Check will try to provide you with additional data on these servers, such as the companies they belong to.</p>
      <p> Visit the <a href="https://github.com/rscmbbng/Border-Check"> project homepage</a> for more information.
      </div>
      <p class='divider'>------------------------------</p>
      </div>
      <div class='toggle' id='legend'> Map legend </div>
      <div id='legend-content'>
      <center><pre>   <img id="home" class='toggle' src='images/markers/marker-icon-0.png'></img>    <img class='toggle' id="hop" src='images/markers/marker-icon-11.png'></img>   <img  class='toggle'id="cluster" src='images/markers/cluster-marker.png'></img>    <img class='toggle' id="destination" src='images/markers/marker-icon-last.png'></img>    </pre></center>
      <div id=legend-text></div></div>
      <p class='divider'>------------------------------</p>
      <div class='toggle' id='attrib'>Who?</div>
      <div id='attrib-content'>
      <p> Border Check is a project by <a href="http://www.roelroscamabbing.nl">Roel Roscam Abbing</a>. Programming by <a href="http://www.lordepsylon.net">Lord Epsylon</a>. Design by <a href="http://bartvanharen.nl/">Bart Van Haren</a>.</p>
      <p>BC was developed during <a href="http://summersessions.net/">Summer Sessions 2013</a> with with the support of <a href="http://v2.nl">V2_ Institute For The Unstable Media</a> at <a href="http://www.laboralcentrodearte.org">Laboral Centro De Arte</a> and the <a href="http://www.mp19.net">MP19 Openlab</a>.
      It uses <a href="http://www.python.org">Python</a>, <a href="http://www.openstreetmap.org">OpenStreetMap</a>, <a href="http://www.leafletjs.com"> Leaflet</a> and <a href="https://github.com/rscmbbng/Border-Check/blob/master/doc/INSTALL"> others.</a></p></div>
      <p class='divider'>------------------------------</p>
      <div class='toggle' id='contact'>Get in touch</div>
      <div id='contact-content'>
      Roel Roscam Abbing (rscmbbng@riseup.net, @rscmbbng) <br />
      psy (epsylon@riseup.net)
      </div>
      
      <div>
      </div>
      </div>
      </div>
      
  </div>
<script type="text/javascript">
  hop_list = """+str(hop_list)+"""
  hop_ip_list = """+str(hop_ip_list)+"""
  counter_max = """+str(last_hop)+"""
  latlong = """+str(geoarray)+"""
  asn_list = """+str(asn_list)+"""
  server_name_list = """+str(server_name_list)+"""
  timestamp_list = """+str(timestamp_list)+"""
  country_code_list = """+str(country_code_list)+"""
  unique_country_code_list = """+str(list(unique_country_code_list))+"""
  </script>
</html>
"""

The FAirQ API provides predictions for air quality parameters including
NO2, PM10, and PM2.5 for Berlin for the next 92 to 106 hours (depending on the availability of the input data).

### Endpoints

The Prediction data can be accessed at various levels (endpoints):

- **/stations**: Get predictions for all measuring stations of the Berliner
  Luftgütemessnetz [Blume](https://luftdaten.berlin.de/lqi). Updated hourly.
- **/streets**: Get predictions on a street-by-street basis. Updated twice a day.
- **/grid**: Get predictions across a grid layout with a spatial resolution of
  50m x 50m (cell size) throughout Berlin. Updated twice a day.
- **/lor**: Get predictions for the "Lebensweltlich orientierte Räume" (LOR),
  which are specific socio-spatial units in Berlin.
- **/simulation**: Get predictions based on simulated traffic scenarios (reduced
  vehicle counts per hour) in selected streets.

### More Information
For further details, please visit the
[press release](https://www.berlin.de/sen/uvk/presse/pressemitteilungen/2024/pressemitteilung.1472028.php)
of the Senatsverwaltung für Mobilität, Verkehr, Klimaschutz und Umwelt and this 
[blog post](https://www.inwt-statistics.com/blog/business_case_air_pollution_forecast) 
by [inwt statistcs](https://www.inwt-statistics.com/).
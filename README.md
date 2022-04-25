# All-Hazard IMT Web Mapping Application 
## Concept Design Document
### March 27, 2022

In anticipation of the wide variety of incidents that All-Hazards IMTs may respond to, we seek to develop a web mapping application that enables streamlined incident monitoring with highly customizable geospatial products. The web application will be constructed with the ArcGIS API for Javascript and will enable users to input features for “all hazards” pertitent to emergency responses, including custom symbols for points, lines, and polygons. 

The project requirements, architecture, and implementation plan are outlined as follows:

#### Project Requirements
Customizable Event Geodatabase
- Excel spreadsheet template for incident-specific event geodatabase
- Python script to create/update/import incident-specific geodatabase to ArcGIS from template
- Expanded incident event symbology based on core of US&R template and NWCG event geodatabase
#### Web Application
- Incident monitoring
- Create, read, update, and delete (CRUD) event data 
- Print format-customizable maps at product (e.g., NWCG) standard
- Permissions for query/approval based on IMT roles (GISS, SITL, IC, etc.)
- Input features based on hand-held data collection (ESRI Field Maps)
- Functional across common hardware and browsers
- Offline functionality with source feature service synchronization of edits

### Architecture Overview

![architecture](images/arch_img.png)

Users: 
As referenced in the figure above, users will be able to interact with the web application both from the browser and via the ArcGIS product suite. All users will be able to interact with the web application through the browser UI. Certain roles (e.g., GISS) will be responsible for “behind the scenes” work via ArcGIS. This will include setting up the event geodatabase (GDB), collecting field data, and maintaining the instanced web map in AGOL.

Browser: The core application UI (“the incident map”) runs on the web browsers of IMT hardware. The application will be designed to work offline, with synchronization occurring after reconnecting to the internet or via sideloading.

Use Cases: 
The core uses of the map application. Includes: monitoring of the incident by the IC and relevant parties (SITL, etc.), user-friendly contributions and updates to map features (including the ability to gate-keep updates behind a permission-based approval workflow), and a printing function that produces maps at desired sizes, formats, and product standards.  

Data: 
The data used by the application in performance of its functions. Includes but is not limited to the instanced WebMap from ArcGIS, presumably specific to a given incident, feature layers included in or viewed separately (e.g., NYC’s PLUTO) from the instanced WebMap, user-generated incident data consistent with the GDB, and users. The users class will include a role property from which certain app functionality will be restricted.  

GDB:
The incident-customizable event geodatabase, generated from an Excel spreadsheet template maintained by the GISSs and other applicable users. 

ArcGIS: 
The ESRI product suite, including ArcGIS Pro, AGOL, and Field Maps.

### Implementation Plan

![implementation](images/impl_img.png)

1. Load a WebMap from the FDNY IMT Org AGOL and feature layers from other data sources (e.g., PLUTO) for development purposes. WebMap will eventually include the custom .gdb as created from an Excel template and accompanying python script.

2. Include an editor that will add, delete, and edit features. Choose appropriate UI for the widget that displays name and symbology of features in the gdb organized by data type (point, line, polygon) or ‘genre’ (e.g., wildfire, collapse, etc.).

3. Develop a printing widget that exports the browser view at predetermined and custom sizes and file formats. The widget should have a toggle (default) that specifies the map be produced at FDNY IMT / NWCG product standards.

4. Define a user class, including roles and permissions. To include but not limited to: Owner, IC, SITL, Logistics, GISS, View-Only. Create a process for managing users. Include web app login and authentication. Develop a feature approval workflow. At minimum, this should include an "Approval Workflow" based on the National Incident Feature Service Workflows. 

5. Build an offline version of the application that is to be sideloaded onto mobile devices. Feature edits in the offline application should write to the “main” map pending role-based approval.

6. Refine all aspects of the user experience, including but not limited to the expanded symbology, the Event GDB template, and the web mapping application. The software should be user-friendly to those with limited technological familiarity. Procure and act upon feedback from expected users.

7. Develop regression testing scripts to be performed after software updates. The scripts should capture the full functionality of the software, including updates/modifications to the event GDB and synchronizing with offline devices.

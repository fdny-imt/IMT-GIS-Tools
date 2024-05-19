import arcpy
from pathlib import Path

__version__ = "2022-09-21"


class CVUpdate:
    """Appends new contingent values from selected table and retires contingent values no longer in the selected table
    Notes:
    - Values in self.persist will always be persisted if it previously existed -- should be set to domain codedvalue
    """
    def __init__(self):
        self.label = "Update Contingent Values"
        self.description = "Update Contingent Values"
        self.canRunInBackground = False
        self.category = "Data Management"
        self.persist_values = {("Other", "Other")}

    def getParameterInfo(self):
        # Define parameter definitions.
        # Refer to https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
        # and https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm

        table = arcpy.Parameter(
            name="Contingent Value Table",
            displayName="Table",
            datatype="DETable",
            parameterType="Required",
            direction="Input",
        )

        gdb = arcpy.Parameter(
            name="GDB to update",
            displayName="Geodatabase to update",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
        )

        return [table, gdb]

    def execute(self, parameters, messages):
        messages.addMessage(f"Running {self.label} version {__version__}")

        for param in parameters:
            messages.addMessage(f"Parameter: {param.name} = {param.valueAsText}")

        # prepare variables for different ways tools require the arguments passed
        gdb = Path(parameters[1].valueAsText)
        cv_table = parameters[0].valueAsText
        
        # for AGP

        # get current domains
        domains = arcpy.da.ListDomains(str(gdb))

        def _do_append(values, table, domain):
            # get domains from cv table
            table_doms = {val[2] for val in values}
            # get existing domains from gdb
            existing_doms = {val for val in [dom.codedValues.keys() for dom in domains if dom.name == domain][0]}
            # get values to append by subtracting what we want from what we have
            to_append = {val for val in values if val[2] in table_doms - existing_doms}

            # get CVs from table
            table_cvs = {(val[1], val[2]) for val in values}
            # get existing CVs from gdb
            existing_cvs = {(val.id, val.values[0].code, val.values[1].code) for val in [cv for cv in arcpy.da.ListContingentValues(str(gdb.joinpath(table)))]}
            # get values to retire by subtracting we want (including values in self.persist) from what we have
            to_retire = {val for val in existing_cvs if (val[1], val[2]) in {(val[1], val[2]) for val in existing_cvs} - table_cvs - self.persist_values }

            # append domains
            for val in to_append:
                arcpy.AddCodedValueToDomain_management(str(gdb), domain, val[2], val[2])
                insert = f"feature_group CODED_VALUE '{val[1]}'; feature_category CODED_VALUE '{val[2]}'"
                arcpy.AddContingentValue_management(str(gdb.joinpath(table)), "FeatureType", insert, )
                # TODO: Add feature template for new value -- someday...no support for this in arcpy

            # retire CVs
            for val in to_retire:
                insert = f"feature_group CODED_VALUE '{val[1]}'; feature_category CODED_VALUE '{val[2]}'"
                arcpy.AddContingentValue_management(str(gdb.joinpath(table)), "FeatureType", insert, retire_value=True)
                arcpy.RemoveContingentValue_management(str(gdb.joinpath(table)), val[0])

        # get values to append from cv table
        fields = ["geom_type", "feat_group", "feat_category", "is_active", "keywords"]
        with arcpy.da.SearchCursor(cv_table, fields, where_clause="is_active=1") as cursor:
            values = [row for row in cursor]

        # get our values to append. use sets to drop duplicate values.

        # groups
        groups_append = set([val[1] for val in values])
        for i in groups_append:
            arcpy.AddCodedValueToDomain_management(str(gdb), "FeatureGroup", i, i)
        
        # TODO: 
        # append domain values and update CVs
        # TODO: Check for existing domains and decide how to handle them
        # TODO: retire CVs that exist in the gdb but not active in the CV table
        # TODO: make sure Other/Other is added to each CV (will have to be removed from list of CVs to retire)
        
        # gather and update domains/cv for feature_categories
        point_vals_append = set([val for val in values if val[0] == "point"])
        poly_vals_append = set([val for val in values if val[0] == "polygon"])
        line_vals_append = set([val for val in values if val[0] == "line"])
        
        _do_append(point_vals_append, "Event_Point", "FeatureCategory(Point)")
        _do_append(poly_vals_append, "Event_Polygon", "FeatureCategory(Polygon)")
        _do_append(line_vals_append, "Event_Line", "FeatureCategory(Line)") 

        # TODO: implement for AGOL

        # TODO:
        # 1. filter rows by is_active == 'Yes' ✅
        # 2. get unique values in feat_group column in each geom_type ✅
        # 3. update feature_group with unique group values (this will apply across all geometry types) ✅
        # 4. for each geom type, update geom feature_category domains ✅
        # 5. update CV's to match values
        # 6. retire CV's in GDB but not in table (or is_active = 0)

        # Todo: Add try/catch to catch cancellations and errors when cleanup is required.

        return

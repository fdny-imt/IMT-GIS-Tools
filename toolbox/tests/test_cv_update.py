import pytest
import arcpy
from toolbox.cv_update import CVUpdate


fields = ["geom_type", "feat_group", "feat_category", "is_active", "keywords"]

data = [
    ("polygon", "Haz-Mat", "Hot-Zone", 1, ""),
    ("polygon", "Haz-Mat", "Cold-Zone", 1, ""),
    ("polygon", "Haz-Mat", "Warm-Zone", 1, ""),
    ("point", "Haz-Mat", "CCP", 1, ""),
    ("point", "Haz-Mat", "Decon", 1, ""),
    ("point", "ICS", "ICP", 1, ""),
    ("point", "Resources", "Engine", 1, ""),
    ("line", "Infrastructure", "Road Closure", 1, ""),
    ("line", "Resources", "Handline", 1, ""),
    ("point", "Resources", "Engine", 1, ""),  # duplicate to test catching of dup values
    ("point", "Haz-Mat", "Not Active", 0, "")  # not active
]

cv_table_name = "Contingent_Values"


class TestCVUpdate:
    # runs execute once, then twice to check that we don't append duplicates
    @pytest.mark.parametrize("runs", [1, 2])
    def test_cv_update(self, messages, egdb, runs):
        cv_table = str(egdb.joinpath(cv_table_name))

        table = str(egdb.joinpath(cv_table_name))
        with arcpy.da.InsertCursor(table, fields) as cursor:
            [cursor.insertRow(row) for row in data]

        # actual test
        cv_update = CVUpdate()
        params = cv_update.getParameterInfo()
        params[0].value = cv_table
        params[1].value = str(egdb)

        for _ in range(runs):
            cv_update.execute(params, messages)

        domains = arcpy.da.ListDomains(egdb)

        domain_group_vals = [
            d.codedValues for d in domains if d.name == "FeatureGroup"
        ][0]

        domain_point_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Point)"
        ][0]

        domain_poly_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Polygon)"
        ][0]

        domain_line_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Line)"
        ][0]

        cv_point = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Point")))
        cv_poly = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Polygon")))
        cv_line = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Line")))

        assert len(domain_group_vals) == 5  # This appends so the default "Other/Unknown" is still there.
        assert len(domain_point_vals) == 5
        assert len(domain_poly_vals) == 4
        assert len(domain_line_vals) == 3
        assert len(cv_point) == 5
        assert len(cv_poly) == 4
        assert len(cv_line) == 3


    def test_retire_cv(self, messages, egdb):
        cv_table = str(egdb.joinpath(cv_table_name))

        table = str(egdb.joinpath(cv_table_name))
        with arcpy.da.InsertCursor(table, fields) as cursor:
            [cursor.insertRow(row) for row in data]

        # actual test
        cv_update = CVUpdate()
        params = cv_update.getParameterInfo()
        params[0].value = cv_table
        params[1].value = str(egdb)

        # append CVs
        cv_update.execute(params, messages)

        # delete cvs from cv_table
        cursor = arcpy.da.UpdateCursor(table, field_names="*", where_clause="feat_group='Haz-Mat'")
        for row in cursor:
            cursor.deleteRow()
        del cursor

        # retire removed CVs
        cv_update.execute(params, messages)

        domains = arcpy.da.ListDomains(egdb)

        domain_group_vals = [
            d.codedValues for d in domains if d.name == "FeatureGroup"
        ][0]

        domain_point_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Point)"
        ][0]

        domain_poly_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Polygon)"
        ][0]

        domain_line_vals = [
            d.codedValues for d in domains if d.name == "FeatureCategory(Line)"
        ][0]

        cv_point = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Point")))
        ret_cv_point = [val for val in cv_point if val.isRetired]
        cv_poly = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Polygon")))
        ret_cv_poly = [val for val in cv_poly if val.isRetired]
        cv_line = arcpy.da.ListContingentValues(str(egdb.joinpath("Event_Line")))

        assert len(domain_group_vals) == 5  # This appends so the default "Other/Unknown" is still there.
        assert len(domain_point_vals) == 5
        assert len(domain_poly_vals) == 4
        assert len(domain_line_vals) == 3
        assert len(cv_point) == 5
        assert len(ret_cv_point) == 2
        assert len(cv_poly) == 4
        assert len(ret_cv_poly) == 3
        assert len(cv_line) == 3

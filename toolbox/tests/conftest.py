import pytest
import arcpy


class Messages:
    def addMessage(self, message):
        print(message)


@pytest.fixture
def messages():
    return Messages()


@pytest.fixture
def test_aprx_path():
    return "toolbox\\tests\\test_aprx\\Test_APRX.aprx"


@pytest.fixture
def egdb(tmp_path):
    gdb = arcpy.CreateFileGDB_management(str(tmp_path), "test.gdb")
    gdb = arcpy.ImportXMLWorkspaceDocument_management(
        gdb, "event_gdb/event_gdb_schema.xml"
    )

    return tmp_path.joinpath("test.gdb")

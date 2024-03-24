# > pip install aspose-cells
from asposecells import Workbook, SaveFormat, JsonUtility, JsonLayoutOptions

def exportToExcel(jsonInput, outputFileName):

    # create a blank Workbook object
    workbook = Workbook()
    # access default empty worksheet
    worksheet = workbook.getWorksheets().get(0)

    # set JsonLayoutOptions for formatting
    layoutOptions = JsonLayoutOptions()
    layoutOptions.setArrayAsTable(True)

    # import JSON data to default worksheet starting at cell A1
    JsonUtility.importData(jsonInput, worksheet.getCells(), 0, 0, layoutOptions)

    # save resultant file in JSON-TO-XLS format
    workbook.save(outputFileName, SaveFormat.AUTO)

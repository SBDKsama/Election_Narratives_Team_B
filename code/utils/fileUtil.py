# Summary:
# The `fileUtil.py` script contains utility functions for interacting with files, specifically focusing on converting JSON data into an Excel format using the Aspose.Cells library.

# Description:
# - The script provides a function `exportToExcel` which takes JSON input and an output file name to create an Excel file.
# - It starts by creating a new Workbook object from the Aspose.Cells library.
# - The default worksheet is accessed and prepared to receive the JSON data.
# - The function sets up `JsonLayoutOptions` to format the JSON data as a table when importing it into the worksheet.
# - The JSON data is imported to the worksheet starting from cell A1.
# - Finally, the workbook is saved in the specified format, which is automatically determined by the file extension provided in `outputFileName`.
# - This function allows for efficient and formatted conversion of JSON data into a more accessible and user-friendly Excel format, facilitating data analysis and reporting.

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

import sys
from pathlib import Path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui     as qtg
from PyQt5 import QtCore    as qtc
import pyodbc
# Sprint-7 Step-1
import copy

class mainWindow(qtw.QWidget):
    # Sprint-4 Step-1
    # This initializer function will execute when an object based on mainWindow is created.
    # Inside this class, self refers to QtWidgets.QMainWindow which is the top level window.
    def __init__(self):
        super().__init__()
        self.cnxn_str = ("DSN=MySQLServer;"
                    "SERVER=DESKTOP-EFKRIC4;"
                    "Database=MountainDb;"
                    "Trusted_Connection=yes;");
        # Sprint-7 Step-2 (Extended previous Sprint-4 Step-2 to
        #                  create a dictionary called self.water_data)
        # Variables to store canvas dimentions and related data
        self.n_rows     = 0
        self.n_columns  = 0
        self.grid_data = []
        self.water_data = {}

        # Sprint-7 Step-3
        # Create a variable that should be used by the anumation's
        # outer-loop, to determine when it should stop. 
        # We create this variable outside the animate() function,
        # so that the variable can also be targeted
        # by other functions in upcoming sprints.
        self.continue_animating = False

        # Sprint-4 Step-3
        # Set window title and position
        self.setWindowTitle("Mountain")
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(qtg.QIcon("../Data/Logo.png"))

        # Sprint-4 Step-4
        # Create a QComboBox called comboBox, that contains
        # the input file names.
        self.comboBox = qtw.QComboBox(self)
        self.comboBox.addItem("trivial.txt")
        self.comboBox.addItem("small.txt")
        self.comboBox.addItem("medium.txt")
        self.comboBox.addItem("large.txt")

        # Sprint-4 Step-5
        # Create label1 and set its initial image. This label will later 
        # be used to display the canvas. You can use any image of a mountain. 
        self.label1 = qtw.QLabel()
        pixmap = qtg.QPixmap("../Data/Logo.png")
        self.label1.setPixmap(pixmap)

        # Sprint-6 Step-1
        # In order to extract mouse click coordinates on the label's image,
        # pin it to the top left corner of the window and prevent scaling
        self.label1.setAlignment(qtc.Qt.AlignTop)
        self.label1.setAlignment(qtc.Qt.AlignLeft)
        self.label1.setScaledContents(False)

        # Sprint-4 Step-6
        # Create label2 to display messages to the user. Set its default
        # text to 'Please wait' and execute its hide() function so that
        # it is not visible when the program starts.
        self.label2 = qtw.QLabel()
        self.label2.setText("Please wait")
        self.label2.hide()

        # Sprint-7 Step-4 (Extended the previous Sprint-5 Step-2 to include
        #                  the self.animate_btn button)
        # Buttons
        # Create a button called loadCanvas_btn. Set its text to 'Display Canvas'.
        # Set its clicked event to execute the loadCanvas function.
        self.loadCanvas_btn = qtw.QPushButton('Display Canvas',clicked=self.loadCanvas)
        # Create a button called loadDb_btn. Set its text to 'Load DB'.
        # Set its clicked event to execute the loadDb function.
        self.loadDb_btn = qtw.QPushButton('Load DB',clicked=self.loadDb)
        # Create a button called animate_btn. Set its text to 'Animate Flow'.
        # Set its clicked event to execute the animate() function.
        self.animate_btn = qtw.QPushButton('Animate Flow',clicked=self.animate) 

        # Sprint-4 Step-8
        # Create a small 10x10 pixel canvas which will later be resized (based on the
        # input file's dimentions). Once the user selected an input file, this canvas
        # will replace label1's mountain image
        self.canvas = qtg.QPixmap(10, 10)        

        # Sprint-7 Step-5 (Extend the previous Sprint-5 Step-3 to include your
        #                  self.animate_btn button in your layout)
        # Create and show() layouts that would display label1 (the mountain image),
        # the comboBox, label2 (hidden), loadCanvas_btn, loadDb_btn and animate_btn.
        layout1 = qtw.QHBoxLayout()
        layout2 = qtw.QVBoxLayout()

        layout1.addWidget(self.label1)

        layout2.addWidget(self.comboBox)
        layout2.addWidget(self.label2)
        layout2.addWidget(self.loadDb_btn)
        layout2.addWidget(self.loadCanvas_btn)
        layout2.addWidget(self.animate_btn)
        layout2.addStretch()

        layout1.addLayout(layout2)

        self.setLayout(layout1)
        self.show()

    # ---------------------------------------------------------------
    # This is the end of the mainWindow class's initializer function.
    # Following are other class functions that are part of the
    # mainWindow class, that are used after the mainWindow object has
    # been initialized.
    # ---------------------------------------------------------------

    # Sprint-5 Step-4
    def loadDb(self):
        # Toggle controls visibility
        self.hideControls()
        self.repaint()

        # Sprint-5 Step-5
        # Extract the selected text from comboBox into a variable 
        # called comboText and use it to read the relevant text input file
        comboText = self.comboBox.currentText()
        file = open(f"../Data/{comboText}", "r")
        f = file.readlines()

        # Sprint-5 Step-6
        # Extract the values of line-1 into self.n_rows and self.n_columns
        temp = f[0].split()
        self.n_rows = int(temp[0])
        self.n_columns = int(temp[1])

        # Sprint-5 Step-7
        # Extract the values of line-2 into a two-dimensional list 
        # called self.grid_data
        # Important! Make sure each value is stored as a valid float
        allvalues = []
        for k in range(1, len(f)):
            temp = f[k].split()
            for x in temp:
                allvalues.append(float(x))

        self.grid_data = [[0.0] * self.n_columns for k in range(self.n_rows)]
        counter = 0
        for c in range(self.n_columns):
            for r in range(self.n_rows):
                self.grid_data[c][r] = allvalues[counter]
                counter = counter + 1

        # Sprint-5 Step-8
        # Prepare items that can be used to lookup/compile the color
        # of each data_point when it is plotted.
        # These colors must be based on the data_point's elevation which
        # is stored in self.grid_data
        allvalues.sort()
        allvalues = list(dict.fromkeys(allvalues))

        inc = 255 / len(allvalues)
        val = 0.0
        colorlist = []

        while not len(colorlist) == len(allvalues):
            colorlist.append('#{:02X}{:02X}{:02X}'.format(int(val), int(val), int(val)))
            val = val + inc

        LookupList = dict(zip(allvalues, colorlist))

        # Sprint-5 Step-9
        # Create a connection (called connection) to your MountainDB 
        connection = pyodbc.connect(self.cnxn_str)
        
        # Sprint-5 Step-10
        # Write the meta data of the text input file to the Files table - if such
        # record does not already exist (perhaps it was created during previous
        # executions of the app).
        # Start by testing to see if such record already exist. Do this by 
        # trying to read a record from the Files table where File_name contains the same
        # value as comboText. 
        cursor = connection.cursor()
        query = "SELECT * FROM MountainDb.dbo.Files WHERE File_name = ?"
        cursor.execute(query, comboText)
        file_record = cursor.fetchone()

        # Sprint-5 Step-11
        # If the record could not be read from the Files table, try to write the file meta
        # data to the Files table - as well as the elevations and color values to the
        # DataPoints table.
        if file_record is None:
            try:
                # Sprint-5 Step-12
                # Insert the record into the Files table. You don't have to pass a
                # value for File_id, since that column is auto generated by the database.
                query = """INSERT INTO MountainDb.dbo.Files (File_name,File_n_columns,File_n_rows) VALUES(?,?,?)"""
                params = (comboText, self.n_columns, self.n_rows)
                cursor.execute(query, params)

                # Sprint-5 Step-13
                # Extract and store the auto generated File_id, since we need to add it
                # to the DataPoints records as a foreign key. 
                cursor.execute("SELECT File_id FROM MountainDb.dbo.Files WHERE File_name = ?", comboText)
                row = cursor.fetchone()
                fileid = row[0]
                
                # Sprint-5 Step-14
                # Insert Grid_Points records. Start by creating a loop that will 
                # execute X number of times - where X is equal to the number of
                # elevation values in the text file.
                for x in range(self.n_columns):
                    for y in range(self.n_rows):
                        # Sprint-5 Step-15 (similar to parts of Sprint-4 Step-16
                        #                  in the mountain_sprint4_skeleton.py file)
                        # Extract the data point elevation
                        elevation = self.grid_data[x][y]
                        # Compile the data point's color
                        color = LookupList[elevation]

                        # Sprint-5 Step-16
                        # Insert the DataPoints record for the current elevation and color value
                        # in the loop. You don't have to pass a value for DataPoint_id, since
                        # that column is auto generated by the database.
                        query = """INSERT INTO MountainDb.dbo.DataPoints (DataPoint_elevation,DataPoint_base_color,File_id) VALUES (?,?,?)"""
                        params = (elevation, color, fileid)
                        cursor.execute(query, params)

                # Sprint-5 Step-17
                # Commit the transaction if all went well, else undo.
                connection.commit()
            except Exception as ex:
                print('Exception Message: '+ str(ex))
                connection.rollback()

        # Sprint-5 Step-18
        # Terminate the connection to your database.
        connection = None

        # Toggle controls visibility
        self.showControls()

    # Sprint-5 Step-21
    def loadCanvas(self):
        # Clear self.grid_data for newly selected map
        self.grid_data = []
        
        # Toggle controls visibility
        self.hideControls()
        self.repaint()

        # Sprint-5 Step-22
        # Extract the selected text from comboBox into a variable 
        # called comboText
        comboText = self.comboBox.currentText()

        # Sprint-5 Step-23
        # Create a connection (called connection) to your MountainDB
        connection = pyodbc.connect(self.cnxn_str)

        # Sprint-5 Step-24
        # Read the record in the Files table where File_name has the same
        # value as comboText
        cursor = connection.cursor()
        query = "SELECT * FROM MountainDb.dbo.Files WHERE File_name = ?"
        cursor.execute(query, comboText)
        file_record = cursor.fetchone()

        # Sprint-5 Step-25
        # Extract the value of File_id from the record - into an integer variable 
        # called file_id.
        # You should use this as filter value when you read the DataPoints records.
        file_id = file_record[0]

        # Sprint-5 Step-26
        # Extract the valies of self.n_rows and self.n_columns from the record.
        # Convert the values to integers before storing them in the variables.
        self.n_rows = file_record[3]
        self.n_columns = file_record[2]

        # Sprint-5 Step-27
        # Read the DataPoints records associated with the Files record you read above.
        # Remember to filter the records based on the foreign key: File_id = file_id
        # Remember to order the records based on the primary key: DataPoint_id
        query = "SELECT DataPoint_id, DataPoint_elevation, DataPoint_base_color FROM MountainDb.dbo.DataPoints WHERE File_id = ?"
        cursor.execute(query, file_id)
        dataPoint_records = cursor.fetchall()
        dataPoint_records.sort()
        # Sprint-5 Step-28 (similar to parts of Sprint-4 Step-16 in 
        #                   the mountain_sprint4_skeleton.py file):
        # Load self.grid_data
        sublist = []
        self.grid_data = []
        # Create a loop that will iterate over all the DataPoints records you read
        i = 0
        for record in dataPoint_records:
            # Create a DataPoint object and populate its variables with the
            # values from the current record in the loop.
            # Ensure that you convert the elevation to a float and the color to a string
            dpObj = DataPoint(record[1], record[2])
            # Append the object to the sublist
            sublist.append(dpObj)
            # If the sublist reached the required size, append
            # it to grid_data and create a new empty sublist
            if (((i + 1) % self.n_columns) == 0):
                self.grid_data.append(sublist)
                sublist = []
            i = i + 1

        # Sprint-4 Step-17
        # Resize the canvas based on the values in n_columns and n_rows
        # and set the canvas as the new image for label1
        self.canvas = qtg.QPixmap(self.n_rows, self.n_columns)
        self.label1.setPixmap(self.canvas)

        # Sprint-4 Step-18
        # Link a painter to label1's image and plot the grid points. 
        painter = qtg.QPainter(self.label1.pixmap())
        for x in range(0, self.n_columns):
            for y in range(0, self.n_rows):
                # Plot the point by extracting its base_color value
                # from the object stored in self.grid_data
                painter.setPen(qtg.QColor(self.grid_data[x][y].base_color))
                painter.drawPoint(x, y)
        painter.end()

        # Toggle controls visibility
        self.showControls()

    # Functions to disable/hide and enable/show controls
    # Sprint-7 Step-6 (Extend previous Sprint-5 Step-19 to also disable
    #                   self.animate_btn)
    def hideControls(self):
        # Disable comboBox
        self.comboBox.setEnabled(False)
        # Show label2
        self.label2.show()
        # Disable loadCanvas_btn
        self.loadCanvas_btn.setEnabled(False)
        # Disable loadDb_btn
        self.loadDb_btn.setEnabled(False)
        # Disable animate_btn
        self.animate_btn.setEnabled(False)
    
    # Sprint-7 Step-7 (Extend previous Sprint-5 Step-20 to also enable
    #                   self.animate_btn)
    def showControls(self):
        # Enable comboBox
        self.comboBox.setEnabled(True)
        # Hide label2
        self.label2.hide()
        # Enable loadCanvas_btn
        self.loadCanvas_btn.setEnabled(True)
        # Enable loadDb_btn
        self.loadDb_btn.setEnabled(True)
        # Enable animate_btn
        self.animate_btn.setEnabled(True)
    
    # Sprint-6 Step-3
    # Add one level of water to the data_point that got clicked,
    # as well as to a square of data_points surrounding it 
    # (10 data_points from the clicked data_point in up, down, 
    # left and right directions).
    # Limit the square to the canvas area (stay within the canvas
    # borders: self.n_columns and self.n_rows)
    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            # Sprint-6 Step-4
            # Get the canvas's clicked x and y coordinates.
            # If you use event.x() and event.y(), you get the
            # coordinates of the mouse click on the window, which
            # includes a border around the label. To get the
            # coordinates of the label, use mapFrom() to extract
            # a QPoint object. 
            QPoint = self.label1.mapFrom(self, event.pos())
            clicked_x = QPoint.x()
            clicked_y = QPoint.y()

            # Sprint-6 Step-5
            # Create a square range around the click event coordinates
            x1 = (clicked_x - 10)
            x2 = (clicked_x + 10)
            y1 = (clicked_y - 10)
            y2 = (clicked_y + 10)
            # Limit the range to the canvas area (stay within the canvas borders)
            if x1 < 0:
                x1 = 0
            if x2 > self.n_columns:
                x2 = self.n_columns
            if y1 < 0:
                y1 = 0
            if y2 > self.n_rows:
                y2 = self.n_rows

            # Sprint-6 Step-6
            # Loop over the square range objects in self.grid_data
            # Do not loop over ALL objects in self.grid_data, but only
            # loop over the objects in the square range you
            # calculated in Sprint-6 Step-5.
            # Note: Technically, the below ranges should have been (x1, x2+1) and
            # (y1, y2+1), but that  would unnecessarily complicate Sprint-6 Step-5,
            # and if you get that wrong, your app will throw an "index out of range"
            # error if the user clicks outside the canvas's border.
            # So let’s keep things simple and make the ranges (x1, x2) and (y1, y2). 
            # Just note that your blue square will now be 20 x 20 data_points instead
            # of 21 x 21 as per the sprint instructions (clicked point + 10 points in
            # both directions = 21 points).
            for x in range(x1, x2):
                for y in range(y1, y2):
                    # Sprint-6 Step-7
                    # Update the data_point's DataPoint object in self.grid_data.
                    # Add 1 unit of water to the object's water_level.
                    self.grid_data[x][y].setwater(self.grid_data[x][y].getwater() + 1)
                    
                    # Sprint-6 Step-8
                    # Update the data_point's color on the canvas by
                    # passing its x and y values to the 
                    # update_data_point_color(x, y) function. 
                    # Do not change the original base_color in the 
                    # DataPoint object in the self.grid_data list, since 
                    # you will re-use the base_color when the water
                    # flowed off the data_point.
                    self.update_data_point_color(x, y)

                    # Sprint-7 Step-8
                    # Add the current DataPoint object's coordinates to
                    # the self.water_data dictionary. Build the "key" part
                    # of the item by concatenating the string representation
                    # of x, plus a slash, plus the string representation of y.
                    # Use an empty string as the "value" part of the item.
                    key = str(x) + "/" + str(y)
                    self.water_data[key] = ""

            # Sprint-6 Step-9
            # Update the canvas after the square's data_point colors have been updated.
            # Note: The Update() function is executed AFTER the caller 
            #       function (mousePressEvent in this case) executed. 
            #       Use it if changes should be shown at once.
            # Note: Repaint() is executed WHILE the caller function is 
            #       still executing. Use it during animations.
            self.update()

    # Sprint-6 Step-10
    # Plot the color of an individual data_point on the canvas.
    # Both the mousePressEvent and the animate (later sprint) functions
    # will have to color individual data_points. To prevent duplicate code
    # in our app, we isolate that functionality in this update_data_point_color
    # function. The mousePressEvent and the animate function can then simply
    # call this function and pass in the x and y indexes of the relevant
    # data_point who's color needs to be updated.
    def update_data_point_color(self, x, y):
        # Retrieve the single data_point's water_level value from its
        # DataPoint object in self.grid_data, but don't make any changes to
        # any data in the object.
        # Use the water_level value to set the data_points new color on
        # the canvas as follows:
        # If water_level < 1, use the base_color in the DataPoint object
        # If water_level = 1, use a light blue color
        # If water_level = 2, use a medium dark blue color
        # If water_level > 2, use a dark blue color         
        if self.grid_data[x][y].getwater() < 1:
            color = self.grid_data[x][y].base_color
        if self.grid_data[x][y].getwater() == 1:
            color = "#ADD8E6"
        if self.grid_data[x][y].getwater() == 2:
            color = "#0000cd"
        if self.grid_data[x][y].getwater() > 2:
            color = "#00008B"

        painter = qtg.QPainter(self.label1.pixmap())
        painter.setPen(qtg.QColor(color))
        painter.drawPoint(x, y)
        # Do not update or repaint the canvas here.
        # It should be done by the caller (mousePressEvent and animate).

    # Sprint-7 Step-9
    def animate(self):
        # Toggle controls visibility
        self.hideControls()
        self.repaint()

        # Sprint-7 Step-10
        # Outer-loop
        # Create an outer-loop that would animate the flow of water
        # until self.continue_animating == False.
        self.continue_animating = True
        while self.continue_animating == True:
            # Sprint-7 Step-11
            # Remove all water from the borders (in both 
            # self.grid_data and self.water_data)
            self.clear_borders()

            # Sprint-7 Step-12
            # In Sprint-7 Step-13 we want to loop over the keys in
            # self.water_data.
            # However, if we do that, we will get a "dictionary changed
            # size during iteration" error, because we are adding and
            # removing items to/from the dictionary at the same time we
            # are looping over the dictionary.
            # Create a new list - called water_copy - and copy the keys
            # in self.water_data to this list. Then loop over this list
            # during the inner-loop at Sprint-7 Step-13.
            water_copy = list(self.water_data.keys())
            # Sprint-7 Step-13
            # Inner-loop
            # Create the inner-loop to process all data_points that still
            # contain water after the borders were cleared above. 
            # Loop over the water_copy list you created above. 
            # If you still get a "dictionary changed size during iteration"
            # error, then you might have to re-think the creation of water_copy
            # to ensure it is an independent collection.
            # The loop will extract each key from water_copy. This key represents
            # the x and y values of the "currently processed" item in the loop.
            for key in water_copy:
                # Sprint-7 Step-14
                # Extract the x and y values from "key" and convert them
                # to integers
                x,y = map(int, key.split("/",1))

                # Sprint-7 Step-15
                # Find the neighbour with the lowest 
                # total-height (elevation + water_level).
                # Pass the x and y values of the currently processed object
                # to self.find_lowest_neighbour(x, y)
                low_x, low_y = self.find_lowest_neighbour(x, y)

                # Sprint-7 Step-16
                # Remove 1 unit of water from the currently processed 
                # DataPoint object's water_level in self.grid_data
                self.grid_data[x][y].setwater(self.grid_data[x][y].getwater() - 1)

                # Sprint-7 Step-17
                # If the water_level of the currently processed DataPoint object in 
                # self.grid_data does not contain any more water (water_level < 1), 
                # then remove the object's coordinates from self.water_data (remove
                # the key from the dictionary)
                if self.grid_data[x][y].getwater() < 1:
                    del self.water_data[key]

                # Sprint-7 Step-18
                # Add 1 unit of water to the lowest neighbour's DataPoint object in 
                # self.grid_data
                self.grid_data[low_x][low_y].setwater(self.grid_data[x][y].getwater() + 1)

                # Sprint-7 Step-19
                # Add the lowest neighbour's DataPoint object's coordinates as a key 
                # to self.water_data
                key = str(low_x) + "/" + str(low_y)
                self.water_data[key] = ""

                # Sprint-7 Step-20
                # Plot the new color of the current DataPoint object
                self.update_data_point_color(x, y)
                # Plot the new color of the neighbour's DataPoint object
                self.update_data_point_color(low_x, low_y)
            self.repaint()

            # Sprint-7 Step-21
            # Stop the animation when there is no more water on the 
            # canvas (when self.water_data is empty)
            if len(self.water_data) == 0:
                self.continue_animating = False

        # Toggle controls visibility
        self.showControls()

    # Sprint-7 Step-22
    # For each one of the four borders, do the following:
    # 1. Loop over all DataPoint objects in self.grid_data that are on the border.
    # 2. Test if the object's water_level > 0, in which case do the following:
    #    2.1 Set the object's water_level = 0;
    #    2.2 Remove the object's coordinates from self.water_data;
    #    2.3 Update the object's data_point color on the canvas by 
    #        calling self.update_data_point_color(x, y).
    #        Do not call the canvas's self.repaint() function here, because that
    #        will be done by the animation() function after all the borders and 
    #        data_points with water have been processed.
    def clear_borders(self):
        # Sprint-7 Step-23 - Top border
        y = 0
        for x in range(self.n_columns - 1):
            if self.grid_data[x][y].getwater() > 0:
                self.grid_data[x][y].setwater(0)
                key = str(x) + "/" + str(y)
                del self.water_data[key]
                self.update_data_point_color(x, y)
        # Sprint-7 Step-24 - Bottom border
        y = self.n_rows - 1
        for x in range(self.n_columns - 1):
            if self.grid_data[x][y].getwater() > 0:
                self.grid_data[x][y].setwater(0)
                key = str(x) + "/" + str(y)
                del self.water_data[key]
                self.update_data_point_color(x, y)
        # Sprint-7 Step-25 - Left border
        x = 0
        for y in range(self.n_rows - 1):
            if self.grid_data[x][y].getwater() > 0:
                self.grid_data[x][y].setwater(0)
                key = str(x) + "/" + str(y)
                del self.water_data[key]
                self.update_data_point_color(x, y)
        # Sprint-7 Step-26 - Right border
        x = self.n_columns - 1
        for y in range(self.n_rows - 1):
            if self.grid_data[x][y].getwater() > 0:
                self.grid_data[x][y].setwater(0)
                key = str(x) + "/" + str(y)
                del self.water_data[key]
                self.update_data_point_color(x, y)

    # Sprint-7 Step-27
    # Search the currently processed object's neighbours to find the one
    # with the lowest total-height (elevation + water_level).
    # The currently processed object is represented by the x and y 
    # values that were passed to this function by the animation's inner loop.
    # If the currently processed object has the lowest total-height, then
    # return its x and y values, else return the x and y values of the neighbour
    # with the lowest total-height.
    def find_lowest_neighbour(self, x, y):
        # Sprint-7 Step-28: Record the currently processed point's total-height
        #                   and coordinates
        lowest_height   = self.grid_data[x][y].elevation + self.grid_data[x][y].water_level
        low_x           = x
        low_y           = y
        # Sprint-7 Step-29: Test neighbour - Top left
        test_height = self.grid_data[x-1][y-1].elevation + self.grid_data[x-1][y-1].water_level
        if test_height < lowest_height:
            low_x = x - 1
            low_y = y - 1
            lowest_height = test_height
        # Sprint-7 Step-30: Test neighbour - Top
        test_height = self.grid_data[x][y - 1].elevation + self.grid_data[x][y - 1].water_level
        if test_height < lowest_height:
            low_x = x
            low_y = y - 1
            lowest_height = test_height
        # Sprint-7 Step-31: Test neighbour - Top Right
        test_height = self.grid_data[x + 1][y - 1].elevation + self.grid_data[x + 1][y - 1].water_level
        if test_height < lowest_height:
            low_x = x + 1
            low_y = y - 1
            lowest_height = test_height
        # Sprint-7 Step-32: Test neighbour - Left
        test_height = self.grid_data[x - 1][y].elevation + self.grid_data[x - 1][y].water_level
        if test_height < lowest_height:
            low_x = x - 1
            low_y = y
            lowest_height = test_height
        # Sprint-7 Step-33: Test neighbour - Right
        test_height = self.grid_data[x + 1][y].elevation + self.grid_data[x + 1][y].water_level
        if test_height < lowest_height:
            low_x = x + 1
            low_y = y
            lowest_height = test_height
        # Sprint-7 Step-34: Test neighbour - Left bottom
        test_height = self.grid_data[x - 1][y + 1].elevation + self.grid_data[x - 1][y + 1].water_level
        if test_height < lowest_height:
            low_x = x - 1
            low_y = y + 1
            lowest_height = test_height
        # Sprint-7 Step-35: Test neighbour - Bottom
        test_height = self.grid_data[x][y + 1].elevation + self.grid_data[x][y + 1].water_level
        if test_height < lowest_height:
            low_x = x
            low_y = y + 1
            lowest_height = test_height
        # Sprint-7 Step-36:  Test neighbour - Right bottom
        test_height = self.grid_data[x + 1][y + 1].elevation + self.grid_data[x + 1][y + 1].water_level
        if test_height < lowest_height:
            low_x = x + 1
            low_y = y + 1
            lowest_height = test_height
        # Sprint-7 Step-37: Return the coordinates of object with the lowest total-height
        return(low_x, low_y)

    # *****************************************************
    # ****** This is the end of the MainWindow class ******
    # *****************************************************

class DataPoint():
    def __init__(self, elevation, color):
        self.elevation      = elevation     # Must be float to cater for data format
        self.base_color     = color
        self.water_level    = 0.0           # Make it a float to simplify calculations that include the elevation

    def setwater(self,v):
        self.water_level = v
    def getwater(self):
        return self.water_level
    # ****************************************************
    # ****** This is the end of the DataPoint class ******
    # ****************************************************

# *******************************************************************************
# This is the Main Code section of the app.
# If you want to, you could put this section and the above classes in separate
# files, and then import the classes into this main code section.
# *******************************************************************************
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # Create a mainWindow object
    mw = mainWindow()
    sys.exit(app.exec())

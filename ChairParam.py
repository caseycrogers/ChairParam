#Author-Casey Rogers
#Description-Create a dogbone for milling
'''
Version 0.1
Current Functionality:
Select two edges that form a <180 degree corner, select a terminating face and specify a diameter.
The add-in will create a dogbone joint between the specified edges a terminating face with the given diameter.

Known Bugs:
Depending on the positioning of the corners and the terminating face, you will get a "zero extent" error.
The dogbone control, when promoted to the create panel, doesn't do anything when pressed.
Symmetry constraint is not maintained when the edges are moved.

Planned Features:
Allow non-planar terminating faces
Improved functionality for non-rightangle corners
Better unit management
Make dogbones respond to changing user parameters
'''

import adsk.core, adsk.fusion, traceback

handlers = []




def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #event handlers
        class chairCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                cmd = args.command
        
                inputs = cmd.commandInputs

                initialVal = adsk.core.ValueInput.createByReal(2)
                inputs.addValueInput('seatAngle', 'Seat Angle (0 - 10 degrees)', 'deg', initialVal)

                initialVal = adsk.core.ValueInput.createByReal(17)
                inputs.addValueInput('seatHeight', 'Seat height (14 - 19 inches)', 'in', initialVal)

                initialVal = adsk.core.ValueInput.createByReal(5)
                inputs.addValueInput('backAngle', 'Back Angle (2 - 10 degrees)', 'deg', initialVal)

                initialVal = adsk.core.ValueInput.createByReal(17)
                inputs.addValueInput('backHeight', 'Back Height (10 - 22 inches)', 'in', initialVal)

                initialVal = adsk.core.ValueInput.createByReal(5)
                inputs.addValueInput('seatAngle', 'Seat Angle (2 - 10 degrees)', 'deg', initialVal)

                initialVal = adsk.core.ValueInput.createByReal(200)
                inputs.addValueInput('chairWidth', 'Chair Width (400 - 600 millimeters)', 'mm', initialVal)
        
                # Connect up to command related events.
                onExecute = CommandExecutedHandler()
                cmd.execute.add(onExecute)
                handlers.append(onExecute)

                #onInputChanged = InputChangedHandler()
        
                #cmd.inputChanged.add(onInputChanged)
                #handlers.append(onInputChanged) 

                #onValidateInputs = ValidateInputsHandler()
                #cmd.validateInputs.add(onValidateInputs)
                #handlers.append(onValidateInputs)
        
        class CommandExecutedHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                app = adsk.core.Application.get()
                ui  = app.userInterface
                try:
                    command = args.firingEvent.sender
            
                # Get the data and settings from the command inputs.
                    app = adsk.core.Application.get();
                    ui = app.userInterface;
                    design = app.activeProduct
                    paramList = design.userParameters
                    for input in command.commandInputs:
                        if input.id == 'seatAngle':
                            seatAngle = paramList.itemByName("SeatAngle")
                            if not seatAngle:
                                ui.messageBox('Missing parameter "SeatAngle"')
                                return
                            seatAngle.expression = input.expression
                        elif input.id == 'edgeSelect':
                            edges = []
                            for i in range(input.selectionCount):
                                edges.append(input.selection(i).entity)
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))
        """class ValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                app = adsk.core.Application.get()
                ui  = app.userInterface
                try:
                    # Get the command.
                    cmd = args.firingEvent.sender
        
                    # Check that two selections are satisfied.
                    for input in cmd.commandInputs:
                        if input.id == 'edgeSelect':
                            if input.selectionCount < 1:
                                # Set that the inputs are not valid and return.
                                args.areInputsValid = False
                                return
                        elif input.id == 'circDiameter':
                            if input.value <= 0:
                                # Set that the inputs are not valid and return.
                                args.areInputsValid = False
                                return
                except:
                    if ui:
                        ui.messageBox('Input changed event failed:\n{}'.format(traceback.format_exc()))"""     

        #add add-in to UI
        cmdDefs = ui.commandDefinitions
        buttonChair = cmdDefs.addButtonDefinition('chairBtn', 'chairParam', 'A GUI for editing the Chair\'s parameters')
        
        chairCommandCreated = chairCommandCreatedEventHandler()
        buttonChair.commandCreated.add(chairCommandCreated)
        handlers.append(chairCommandCreated)

        createPanel = ui.toolbarPanels.itemById('SolidCreatePanel')
        
        buttonControl = createPanel.controls.addCommand(buttonChair, 'chairBtn')
        
        # Make the button available in the panel.
        buttonControl.isPromotedByDefault = True
        buttonControl.isPromoted = True
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        cmdDef = ui.commandDefinitions.itemById('chairBtn')
        if cmdDef:
            cmdDef.deleteMe()
        createPanel = ui.toolbarPanels.itemById('SolidCreatePanel')
        cntrl = createPanel.controls.itemById('chairBtn')
        if cntrl:
            cntrl.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc))
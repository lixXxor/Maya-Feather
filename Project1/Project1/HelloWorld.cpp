#include "HelloWorld.h"
#include <maya/MFnPlugin.h>
#include <maya\MItSelectionList.h>
#include <maya\MDagPath.h>
#include <maya\MItMeshVertex.h>

void* HelloWorld::creator() { return new HelloWorld; }

MStatus HelloWorld::doIt(const MArgList& argList) {
	MGlobal::displayInfo("Hello World!");
	//Get list of selected items
	MSelectionList selectedItem;
	//Get list of selected items for realsies
	MGlobal::getActiveSelectionList(selectedItem);
	MStatus stat;
	//Iterate through them.
	MItSelectionList it(selectedItem);

	while (!it.isDone() ) {
		MDagPath dagPath;	//Will hold a path to the indexed object
		MObject component;	//List of selected components

		it.getDagPath(dagPath, component);

		MFnDependencyNode fn(dagPath.node());
		MString status = "OBJECT: ";
		status += fn.name().asChar();
		MGlobal::displayInfo(status);

		if (!component.isNull()) {
			MGlobal::displayInfo("Is not null!");
			MItMeshVertex itVert(dagPath, component, &stat);

			if (stat == MS::kSuccess)
			{
				while (!itVert.isDone())
				{
					
					MPoint point = itVert.position(MSpace::kWorld);
					MString pointStr;
					pointStr += itVert.index();
					pointStr += "\t";
					pointStr += point.x;
					point.x += 10;
					pointStr += "\t";
					pointStr += point.y;
					pointStr += "\t";
					pointStr += point.z;
					MGlobal::displayInfo(pointStr);
					itVert.setPosition(point, MSpace::kWorld);

					itVert.next();
				}
			}
		}
		else{
			MGlobal::displayInfo("Is null.. :(");
		}
		it.next();

	}



	return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
	MFnPlugin plugin(obj, "Featherizer Group", "1.0", "The Best");
	MStatus status = plugin.registerCommand("helloWorld", HelloWorld::creator);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	return status;
}

MStatus uninitializePlugin(MObject obj) {
	MFnPlugin plugin(obj);
	MStatus status = plugin.deregisterCommand("helloWorld");
	CHECK_MSTATUS_AND_RETURN_IT(status);
	return status;
}
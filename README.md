# Select Connected Faces by Normals - Blender Addon

![](images/Banner.png)

## Installation
1. Right click [**this link**](https://raw.githubusercontent.com/japuzen/bpy-SelectFacesByNormals/master/Select_Faces_by_Normals_Addon.py) and click *Save Link As* to download the Python file.
2. In Blender, go to *Edit > Preferences*.

![](images/Addon%20Doc%20-%20Edit>Preferences.png)

3. In *Addons* click *Install* and find the *Select_Faces_by_Normals_Addon.py* file.

![Image of Full Pack](images/Addon%20Doc%20-%20Addon%20Install.png)

4. Click the checkbox to the left of the addon to enable it.

## Usage
1. Select an object and go into Edit mode
2. Select one or multiple faces
3. Click the ***Select Connected Faces by Normals*** operator at the bottom of the ***Select*** dropdown menu. You can also use the *Search* function in Blender to find the operator (the default keybinding is F3).

![](images/Select%20Dropdown.png)

![](images/Select%20Faces%20Operator.png)

4. A menu panel will pop up on the bottom left corner of the 3D Viewport. You can use this to change the Angle Limit and Group Angle Limit.

![](images/Panel.png)

## Info

![](images/Side.png)

This add-on takes a face or faces on an object that were selected by a user and expands the selection to connected faces whose normal vectors meet a specified criteria. Connected faces who all meet the critera set by the *Angle Limit* and *Group Angle Limit* are grouped together. A face is added to a group only if the following are true:
1. It is connected to a face that is in the group
2. The difference between the face's normal and the connected face's normal is less than the *Angle Limit*
3. The difference between the face's normal and the group's total normal is less than the *Group Angle Limit

I originally made this as a way to select flat surfaces in scan files. The angle limits can be adjusted depending on how noisy a surface is. A smoother surface would need smaller angle limits, and vice versa.

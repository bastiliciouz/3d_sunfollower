# 3d_sunfollower
Easy way to follow the sun with 2 servos and photo resistors

- First of all: Yes, the comments within the code are in German. Just give me a hint whether you need it in English and I'll translate it.
- And second: Python newbie, please be patient. Thanks!
- Needed hardware beside Raspberry: ADS1115 ad-converter, PCA9685 servo driver and some servos (in my case MG996R).
- A bit technical understanding and experience with soldering iron ;-)

The idea behind the code is not new:
Follow the sun or any other light source by analysing some sensors and steer the motors accordingly.

This code will make you able to read out the values of 4 resistors to steer 2 servos X/Y dimensional to follow the location of your light source.
For analysis I further implemented some lines to store the values in case of changes to a simple MySQL database. For user data of the db either directly add them to the code or import a new file as I did.

Sequences in a nutshell:
- Initialize each and everything (sensors and servos)
- Verify the difference between crossed sensors
- Steer horizontal and/or vertical servo until values of sensors are more or less comparable (threshold can be set)
- Avoid any servo moves beyond 0° and 180° limit
- Store changes to DB when applicable

Any questions? Don't hesitate to contact me.
BR Bastian

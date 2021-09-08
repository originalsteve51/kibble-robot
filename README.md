This is a project I have made using a Raspberry Pi to control a stepper-motor driven cat feeder.

This cat feeder drops food from a chute into a bowl. The bowl is mounted on a platform incorporating
a strain-gauge that is monitored so the weight of the food in the bowl is known.

A cereal-type food dispenser is used. It consists of: 
- A hopper into which dry cat food is poured
- A rotary paddle wheel which, when turned, causes the food to drop into a chute

The chute is positioned so that it directs food into a cat dish.

The control program **feeder.py** checks the weight of food in the cat dish several times a day. If the
weight is below a certain value, the stepper motor is driven to deposit more food into the bowl. This
continues until the weight of food reaches the desired value. 

As a safety measure, the number of times
the motor turns is capped to a maximum value. This is to prevent run-away feeding, a situation that 
occurred once when my Roomba vacuum cleaner disconnected the strain gauge. Run-away feeding in that case caused
all of the food to be dispensed because the strain gauge scale was reading 0.00 continuously.

There is more to this project. I plan to update this document sometime in the future!

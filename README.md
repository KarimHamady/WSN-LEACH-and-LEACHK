# Disclaimer
The code is not thoroughly tested and for sure contains unintended behaviour (I had a tight deadline :) ) But I'm open for any improvements, just open a PR!

# Code File Structure
1. helperFunctions.py contains distance calculation and propagation delay functions as well as wave velocity and the parameters.py is imported inside
2. LEACH.py and LEACHK.py contain the class definition of each protocol (Calculation in setup and steady phase, visualization and some useful methods)
3. Node.py and Packet.py contains the class definition for creating the simulation (Building block for sending packets between node)

In the main.py you can choose to run LEACH, LEACH-K protocols as well as drawing the elbow in K-means Leach

# WSN-LEACH-and-LEACHK
1. Drawing the Elbow in K-means
![image](https://github.com/KarimHamady/WSN-LEACH-and-LEACHK/assets/113800496/8d0e591a-13e0-4619-b4f6-03e2937c6cbc)

2. LEACH Visualizer
![image](https://github.com/KarimHamady/WSN-LEACH-and-LEACHK/assets/113800496/ec0c3622-4d37-4e47-bdab-f8ab8812330f)

3. Results & Interpretation
![image](https://github.com/KarimHamady/WSN-LEACH-and-LEACHK/assets/113800496/572b23bc-6746-4a7e-a227-b183ce796af8)

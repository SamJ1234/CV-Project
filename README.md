# CV-Summer-Project
Our goal is to make a device that counts the number of tic tacs in an image or video. 
The python scripts here do that by importing the OpenCV library, as well as others.

All programs can take a live picture. They can be changed to process a pre-saved image 
by commening out any lines contatining "camera" and adding image=imread("link to image").

Separated Tic Tacs: All programs work for separated tic tacs.
                    Blob Detection is the most accurate and can also discriminate between tic tacs and rice using the area filter. 
Touching Tic Tacs: The watershed file detects touching tic tacs about 40% of the time.

Note: The camera can support 10809 at 30fs and 2592x1944p still images. Some of the programs reduce that resolution, as it causes the output image re-sizing to not work. The output images are always re-sized because my screen is only 7".

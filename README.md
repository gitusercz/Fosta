# Fosta

A raspbery pi based security cam, that alarms, when post arrives. 

## 1 Plot

There is a hungarian post type, that is "in hand" (ajánlott). Those cannot land into the postbox, but into the recipient's hands only. Postmen do not necessarily use the doorbell and wait for you. They have a built in doorbell: car horn. So they show up, horn, and if you happen to show up immediately you might get your letter.

If not, the postman writes a notification that letter could not be delivered, therefore you are welcome in the following two weeks at the post office on the other half of the city in worktime.

## 2 Setup

For convenience I have a custom built postbox with plexi doors, so you do not have to open it, to see if you have mail. I have installed a Raspberry Pi with camera to watch it.

## 3 How it works

1. The Raspberry Pi takes a photo every X seconds (set in config file)

2. Photo is rotated

3. Photo is cropped (ROI is just a 45 x 38 pixel area)

4.  Photo converted to grayscale

5.  Variance is calculated on the pixel values

6.  If variance value is above limit, it sends an email

7.  Jump to step 1

### 3.1 Support files
1. Folder: IMG - saved images are stored here.
2. Folder: resources - Git support files are here (images for demonstration, not used by the script)
3. BWC.py - Main script. 
4. BWC_log.txt - a logfile for  application start timestamps
5. config.ini - file to change script behavior, like ROI pixel coordinates, detection variance limit, check frequency in seconds. 
6. credentials.yml - confog file for mail sending setup
7. sendagmail.py - gmail sending handler

## 4 Images of the setup

### 4.1 What the camera sees when postbox is empty
![Empty postbox](/resources/01_empty.jpg)

### 4.2 What the camera sees when mail arrived
![Mail arrived](/resources/02_full.jpg)
### 4.3 Mail notification
![Notification e-mail](/resources/03_e-mail.png)

## 5 Further use: Security cam

This project was based on [BWC](https://github.com/gitusercz/BWC), which was a webserver with periodically updating image. Fosta was built on top of this. Practically, a webserver is set up and the displayed HTML is edited upon each iteration.

## 6. Notes

### 6.1 On "Variance"

When I was looking for a statistical value that represents that "there is something" on the picture I was browsing through numpy possibilities. According to wikipedia, variance seemed a good candidate. After trying out different pre-saved imagess, it turned out to be a working one. 
[Variance](https://en.wikipedia.org/wiki/Variance)  is a measure of [dispersion](https://en.wikipedia.org/wiki/Statistical_dispersion "Statistical dispersion"), meaning it is a measure of how far a set of numbers is spread out from their average value.

### 6.2 On "Fosta"
This is a name coined by a frustrated SW developer earlier. He created a website to log end user complaints for the faulty work of the Hungarian Post. [The webpage is down.]([https://444.hu/2019/12/03/egy-kiborult-programozo-ugy-dontott-felveszi-a-harcot-a-magyar-postaval-ebbol-lett-a-fosta](https://444.hu/2019/12/03/egy-kiborult-programozo-ugy-dontott-felveszi-a-harcot-a-magyar-postaval-ebbol-lett-a-fosta))

 

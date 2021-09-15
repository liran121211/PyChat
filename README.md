
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://i.ibb.co/VmhxMV2/pychat-logo.png" alt="Logo" width="672" height="378">
  </a>

  <h3 align="center">PyChat</h3>

  <h4 align="center">
    The easiest way to communicate with people around the world!
    <h4 />



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#limitations">Limitations</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

When I was looking to build a unique project, I wanted to include a server side that would allow to interact with people outside the local network. I started building a client side and a server side so they could pass messages between them.
With the service of [DigitalOcean](https://m.do.co/c/70ab03cd54f1) I managed to fully operate server that performs operations according to the command it receives from the client.

Realizing the potential of this architecture I decided to take the idea one step further and build a multiplayer chat that would allow messages to be delivered between anyone who would use the app. 

The whole system was built in Python so I wanted to use the latest design libraries available to the user.
The entire graphical user interface was built using PyQT5.

As I progressed with building the app I realized I needed another model that would allow users to be different from each other, so I added database model using PostgreSQL which is also being part of the server.


**Here's why I choose to make a chat application:**
* It is scalable project: Nowadays, there are a lot of features that enhance the user experience, Therefore the chat can always be changed and upgraded
* It is an excellent alternative chat services currently offered (
* The process of building such application requires a lot of knowledge such as Threads and Design Patterns, SQL.

### Built With

* [PyQT5](https://doc.qt.io/)
* [PostgreSQL](https://www.postgresql.org/)
* [Sockets](https://docs.python.org/3/howto/sockets.html)



<!-- GETTING STARTED -->
## Getting Started

In order to run the app, please follow the instructions:

### Prerequisites

According to the application, the below plugins must be installed, whether through PyCharm Virtual Environment or CMD Windows Environment.

Python Interpreter 3.7 and above
[Python 3.7.0](https://www.python.org/downloads/release/python-370/)
 
 PyQT5
  
  ```pip install PyQt5==5.15.4```
  
   Requests
  
  ```pip install requests==2.26.0```

   PlaySound2
  
  ```pip install playsound2==0.1```


### Installation

1. The application can be run through Python interpreter or executable file.
	[Python Version](https://github.com/liran121211/PyChat/archive/refs/heads/master.zip)
	[EXE Version](http://167.172.181.78/PyChat.zip)


## Screenshots

 **<u>**Loading Window**</u>**:
  
Fetching sound and images files, establishing connection to server, and check the status of the SQL database. 
	
![enter image description here](http://167.172.181.78/screenshots/loading_window.png)

 **<u>**Login Window**</u>**:
  
 Only registered user can access the chat application.
 
 ![enter image description here](http://167.172.181.78/screenshots/login_window.png)

 **<u>**Register Window**</u>**:
  
Fast register page, other user parameters are randomly generated.

![enter image description here](http://167.172.181.78/screenshots/register_window.png)
  
  **<u>**Main Chat Window**</u>**:
  
After successful login, the chat window will be loaded with the real-time data from the server, Includes: Online Users, Chat Rooms.
![enter image description here](http://167.172.181.78/screenshots/main_chat1.png)

![enter image description here](http://167.172.181.78/screenshots/main_chat2.png)
 
 ![enter image description here](http://167.172.181.78/screenshots/settings_panel.png)
 
 ![enter image description here](http://167.172.181.78/screenshots/about_panel.png)
<!-- ROADMAP -->
## Features

 - Online users list that updates in real-time.
 - Room chat list that updates in real-time.
 - Search users by keyword.
 - Make conversations with users in different chat rooms by joining or leaving rooms.
 - Change your avatar image with a click.
 - Change your username color with a click.
 - Logout to the Login Page.
 - Turn On/Off sound effects of the application.
 - See all of the copyrights related to the application.
 - Auto disconnection from the chat if server goes down.
 - Fast registration process.

<!-- CONTRIBUTING -->
## Limitations

To avoid problems when using the app, please note the following limitations:

1. Fetching new avatar image is limited at some point, abusing this feature will effect the users in the system.
2. Any attempt to over flood the chat with messages will effect the performance of the server.
4. Only one chat room can remain active at that moment, any move to another room will prevent receiving messages to the previous room you left.



<!-- LICENSE -->
## License

Distributed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) License. 



<!-- CONTACT -->
## Contact

Liran Smadja - [@LinkedIn](https://www.linkedin.com/in/liran-smadja/) - liransm@ac.sce.ac.il

Other Projects: [See Now!](https://github.com/liran121211)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

<html><head></head><body><p style="text-align: center;">© All rights reserved to Liran Smadja ©</p>
<p style="text-align: center;"><span style="text-decoration: underline;">Avatars Provided by:</span></p>
<p style="text-align: center;">2020-2021 (c) Gie Katon (https://giekaton.com)<br>Multiavatar - Multicultural Avatar Maker<br><a href="https://multiavatar.com">https://multiavatar.com </a></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">Main Chat Icons Provided by:</span></p>
<p style="text-align: center;">© 2010-2021 Freepik Company S.L. All rights reserved</p>
<p style="text-align: center;">Sound Icon: <a class="author-name line-height-sm" href="https://www.flaticon.com/authors/those-icons">Those Icons</a></p>
<p style="text-align: center;">Mute Icon: <a class="link--normal mg-right-lv1" href="https://www.flaticon.com/authors/pixel-perfect/filled">Pixel Perfect Filled</a></p>
<p style="text-align: center;">About Icon: <a class="link--normal mg-right-lv1" href="https://www.flaticon.com/authors/freepik/others"> Others </a></p>
<p style="text-align: center;">Search Icon(icon-icons.com): <a class="icons-label" title="Designer" href="https://icon-icons.com/users/1QnM3XSnrA8aVK8veYati/icon-sets/">Lineicons</a></p>
<p style="text-align: center;">Username Color Change: <a class="link--normal" title="More icons from Art and design pack" href="https://www.flaticon.com/packs/art-and-design">Art and design</a></p>
<p style="text-align: center;">Avatar Icon Change: <a class="link--normal" title="More icons from Teamwork pack" href="https://www.flaticon.com/packs/teamwork-71">Teamwork</a></p>
<p style="text-align: center;">Settings: <a class="link--normal" title="More icons from Help &amp; support pack" href="https://www.flaticon.com/packs/help-support-2">Help &amp; support</a></p>
<p style="text-align: center;">Send Button: <a href="https://www.pngkit.com/view/u2w7q8u2o0y3e6t4_send-button-png-send-button-icon-png/">PNGKit</a></p>
<p style="text-align: center;">Logout Button: <a href="https://www.flaticon.com/authors/freepik">Freepik</a></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">Chat Rooms Icons Provided by:</span></p>
<p style="text-align: center;"><span class="copyright m0 single-spcr">© 2021 InVisionApp Inc. All&nbsp;rights&nbsp;reserved.</span></p>
<p style="text-align: center;"><a href="https://www.invisionapp.com"><span class="copyright m0 single-spcr">https://www.invisionapp.com</span></a></p>
<p style="text-align: center;"><a href="https://www.invisionapp.com/inside-design/free-holiday-icons/">Kristin Hillery</a></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">Window Logos:</span></p>
<p style="text-align: center;">2021 © Background Generator - BgGenerator.com. All rights reserved</p>
<p style="text-align: center;"><a href="https://bggenerator.com">https://bggenerator.com</a></p>
<p style="text-align: center;">Pixlr © Inmagine Lab Pte Ltd 2021. All rights reserved.</p>
<p style="text-align: center;"><a href="https://pixlr.com">https://pixlr.com</a></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">Login Icons Provided by:</span></p>
<p style="text-align: center;">© 2021 IconArchive.com</p>
<p style="text-align: center;">Password Icon: <a href="https://iconarchive.com/artist/icons8.html">Icons8</a></p>
<p style="text-align: center;">Username Icon: N/A</p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">App Icon Provided by:</span></p>
<p style="text-align: center;">Created by: John Sorrentino Copyright 2021</p>
<p style="text-align: center;"><a href="https://favicon.io/">https://favicon.io/</a></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><span style="text-decoration: underline;">App Sound Effects Provided by:</span></p>
<p style="text-align: center;">Â© 2019 Zapsplat</p>
<p style="text-align: center;"><a href="https://www.zapsplat.com">https://www.zapsplat.com</a></p>
<p style="text-align: center;">&nbsp;</p></body></html>
<p style="text-align: center;"><span style="text-decoration: underline;">Client/Server Architecture Concept:</span></p>
<p style="text-align: center;">2021 © קמפוס IL - המיזם הלאומי ללמידה דיגיטלית</p>
<p style="text-align: center;"><a href="https://www.zapsplat.com">https://campus.gov.il</a></p>
<p style="text-align: center;">&nbsp;</p></body></html>


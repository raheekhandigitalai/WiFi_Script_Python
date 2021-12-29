# WiFi_Script_Python

The purpose of this script is to allow us to perform custom steps on mobile devices hosted on a SeeTest Cloud instance.

This script will be triggered as part of the cleanup mechanism.

Prerequisites:

1. Enable Webhook Cleanup in SeeTest Cloud on a global level
   1. Login as a Cloud Admin
   2. Navigate to Settings > Device Policies
   3. Enable Webhook Cleanup
   
    In the configure section, we need to populate the relevant fields, but we'll come back to this. We need to enable the Webhook Cleanup on a global level so that it can be invoked on a project level. 


2. Enable Webhook Cleanup in SeeTest Cloud on a project level
   1. Login as a Cloud Admin
   2. Navigate to Settings > Project > Select your Project > Manage
   3. Navigate to Device Policies
   4. Enable Webhook Cleanup
   

3. Create a CICD Job (I used Jenkins, Freestyle project)

    There are a couple of things to keep in mind:


   a. since we are trying to invoke the job automatically as soon as a device is released, we need to configure the job to allow to be triggered remotely.

   ![img.png](img.png)


   b. Authentication Token is generated from Manage Jenkins > Manage Users > Select User > Configure. Under Configure, Create a new API Token.
   
   ![img_1.png](img_1.png)

   c. We need to parameterize the build by enabling "This project is parameterized". For this I installed EnvInject Plugin.    

   ![img_2.png](img_2.png)

   ![img_3.png](img_3.png)

   These will be important and referenced in the code WiFiScript.py, they are defined in the following way:

       import os
       
       uid = os.getenv("deviceID")
       operating_system = os.getenv("deviceOS")

   They can then be referenced respectively depending on what I need to do. When initializing the session, since we don't know to being with which device is getting cleaned up, this is how I am providing the capabilities, and I let Jenkins inform us on the deviceID based on the job:

       capabilities['udid'] = '%s' % uid

   d. When I tried to invoke the code, I was getting an error message regarding needing a CrumbIssuer. 

   CrumbIssuer represents an algorithm to generate a nonce value, known as a crumb, to counter cross site request forgery exploits. Crumbs are typically hashes incorporating information that uniquely identifies an agent that sends a request, along with a guarded secret so that the crumb value cannot be forged by a third party. 

   According to online sources, there are a number of ways to tackle this, I choose the easiest option to simply disable the csrf check from Jenkins by running a script (_Not recommended in production_)

   From Manage Jenkins > Script Console, I ran following snippet:   
                  
                     import jenkins.model.Jenkins
                     def instance = Jenkins.instance
                     instance.setCrumbIssuer(null)

   d. 
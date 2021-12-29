# WiFi_Script_Python

The purpose of this script is to allow us to perform custom steps on mobile devices hosted on a SeeTest Cloud instance.

This script will be triggered as part of the cleanup mechanism.

Prerequisites:

1. Populate the relevant fields in the **config.properties** file, the following fields are available:

```
[seetest_authorization]
access_key_admin=<>
access_key_cleanup=<> - Can be obtained by logging in to SeeTest Cloud as Cloud Admin > Settings > Device Policies > Click on Key Icon to reveal Access Key of Cleanup User

[seetest_urls]
cloud_url=http://<seetest_cloud_url>:<port>
end_point=/api/v1/devices

[tags]
good_tag_value=GoodWiFi - String value of tag we want to provide to a device if it is connected to CORRECT WiFi
bad_tag_value=BadWiFi - String value of tag we want to provide to a device if it is connected to INCORRECT WiFi

[wifi]
wifi_name=WiFiName - String value of the WiFi connection we are looking for on the device
```

2. Enable Webhook Cleanup in SeeTest Cloud on a global level
   1. Login as a Cloud Admin
   2. Navigate to **Settings > Device Policies**
   3. Enable Webhook Cleanup
   
    In the configure section, we need to populate the relevant fields:


   ![img_4.png](img_4.png)

   The URL is the full JOB URL:

```
https://<jenkins_url>/job/<job_name>/buildWithParameters?=Token
```

  And the Authorization Header Value is Cloud Admin credentials. If you don't have this format handy, a quick and easy way is to open up Postman, and populate the Authorization field like this choosing **Basic Auth**:

  ![img_5.png](img_5.png)

  When exporting this to code, it will show the proper format (_Code Export Language does not matter_):

  ![img_6.png](img_6.png)

3. Enable Webhook Cleanup in SeeTest Cloud on a project level
   1. Login as a Cloud Admin
   2. Navigate to **Settings > Project > Select your Project > Manage**
   3. Navigate to **Device Policies**
   4. Enable Webhook Cleanup

  Enabling it on a Project Level allows us to invoke the CICD Job when cleanup is triggered on the devices for that project.   

4. Create a CICD Job (_I used Jenkins, Freestyle project_)

    There are a couple of things to keep in mind:


   a. since we are trying to invoke the job automatically as soon as a device is released, we need to configure the job to allow to be triggered remotely using Auth Token:

   ![img.png](img.png)


   b. Authentication Token is generated from Manage Jenkins > Manage Users > Select User > Configure. Under Configure, Create a new API Token (_Should be on an admin role or user who created the project_):
   
   ![img_1.png](img_1.png)

   Populate the Token in the Jenkins Job under **Build Triggers > Trigger Builds Remotely**, as well as in the **Webhook Cleanup Rule** as per Step 1.

   c. We need to parameterize the build by enabling "This project is parameterized". For this I installed EnvInject Plugin.    

   ![img_2.png](img_2.png)

   ![img_3.png](img_3.png)

   These will be important and referenced in the code **WiFiScript.py**, they are defined in the following way:

```
import os
       
uid = os.getenv("deviceID")
operating_system = os.getenv("deviceOS")
```

   They can then be referenced respectively depending on what we need to do in the script. When initializing the session, since we don't know which device it will pick to begin with, we need to let the Jenkins job device that, depending on which device is getting cleaned up at the time. This is how should define the device setup in the capabilities:


```
capabilities['udid'] = '%s' % uid
```

   d. When I tried to invoke the code, I was getting an error message regarding needing a CrumbIssuer. 

   CrumbIssuer represents an algorithm to generate a nonce value, known as a crumb, to counter cross site request forgery exploits. Crumbs are typically hashes incorporating information that uniquely identifies an agent that sends a request, along with a guarded secret so that the crumb value cannot be forged by a third party. 

   According to online sources, there are a number of ways to tackle this, I choose the easiest option to simply disable the csrf check from Jenkins by running a script (_Not recommended in production_)

   From Manage Jenkins > Script Console, I ran following snippet:   
       
```           
import jenkins.model.Jenkins
def instance = Jenkins.instance
instance.setCrumbIssuer(null)
```
   
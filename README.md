# WiFi_Script_Python

The purpose of this script is to allow us to perform custom steps on mobile devices hosted on a SeeTest Cloud instance.

This script will be triggered as part of the cleanup mechanism.

Prerequisites:

1. Enable Webhook Cleanup in SeeTest Cloud on a global level
   1. Login as a Cloud Admin
   2. Navigate to Settings > Device Policies
   3. Enable Webhook Cleanup
   
    In the configure section, we need to populate the relevant fields, but we'll come back to this. We need to enable the Webhook Cleanup on a global level so that it can be invoked on a project level. 


3. Enable Webhook Cleanup in SeeTest Cloud on a project level
   1. Login as a Cloud Admin
   2. Navigate to Settings > Project > Select your Project > Manage
   3. Navigate to Device Policies
   4. Enable Webhook Cleanup
   

3. Create a CICD Job (I used Jenkins)

    There are a couple of things to keep in mind:

   1. since we are trying to invoke the job automatically as soon as a device is released, we need to configure the job to allow to be triggered remotely 

4. 
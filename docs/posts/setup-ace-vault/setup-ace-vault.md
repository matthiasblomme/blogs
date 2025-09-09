# **UPDATE ALL SCREENS AND REF**

https://cronos-my.sharepoint.com/personal/blommma_cronos_be/_layouts/Doc.aspx?sourcedoc={5170FF6E-20E5-44DB-A0F3-8224B5FDD7D5}&wd=target%28Projecten%2FLuminus.one%7CD91EB0E3-5419-461F-BD9F-6F31F291568A%2FCreate%20vault%7C4BACE255-85DB-459E-BE39-AAC2ADAAF4A7%2F%29&wdpartid={3C25575D-4178-015C-3D85-D791AB9620D1}{1}&wdsectionfileid={D91EB0E3-5419-461F-BD9F-6F31F291568A}
onenote:https://cronos-my.sharepoint.com/personal/blommma_cronos_be/Documents/Matthias%20@%20Cronos/Projecten/Luminus.one#Create%20vault&section-id={D91EB0E3-5419-461F-BD9F-6F31F291568A}&page-id={4BACE255-85DB-459E-BE39-AAC2ADAAF4A7}&object-id={D92AE8CA-1518-0A22-14BB-297BA14D7CD8}&A2


> what if vault share goes down?

About
The IBM ACE vault is set to replace the older (and less secure) dbparms setup.

There are 2 new commands that you need to know about that will replace mqsisetdbparms
	• mqsivault to create a vault store
	• mqsicredentials to encrypt and store the credentials in the vault

There are 3 types of vault
 - Integration node vaults: shared over all node owned processes (server, http listener, …)
 - Integration server vaults: only used by one integration server and stored inside the work directory
 - External vaults: these are vaults that are stored externally from the node or server and, unfortunately, are not yet supported by the loud operator.

Depending on your environment, you might need one or the other (if you run Node based or only with Standalone Integration server)
Let's assume we are running on a cloud setup and only focus on the Integration server vaults.








Setup
Let's prepare our local environment. Start by creating a standalone integration server, either via the toolkit




Or via the command line if you prefer. But the toolkit offers you some management capabilities that will make your life easier.



Make the required adjustments to overrides/server.conf.yaml file, restart the integration server and deploy your libraries and applications.



Next up, the vault.

Creating a vault
Now that we have an integration server setup, let's inject some credentials.

Start by creating the vault itself. This is done with the mqsivault command, 



You need a stopped integration server for this to work, so stop the IS again and create the vault

C:\Program Files\IBM\ACE\12.0.12.5>mqsivault --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --create --vault-key someVaultKey
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP8071I: Successful command completion.

You can verify that the vault has been created by looking at the IS config directory, you will see a new folder with the name vault



Inserting credentials
An empty vault isn't really that usefull, so let insert some dummy credentials and print them out afterwards.
Inserting credentials can be one with the mqsicredentials command




The output of this command is quite big, but have a look at it anyway. The basics you need to know are this
mqsicredentials --work-dir <location of your IS> --create --vault-key <key of the previously made vault> --credential-type <type of the credential> --credential-name <name of the credential> --…

Based on the credentials type, you will have to specify other parameters, like
	• --username
	• --password
	• --apikey
	• --access-token
	• …

A simple example of inserting a credentials is setting the broker truststore password
C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --create --vault-key someVaultKey --credential-type truststore --credential-name password --password somePassword
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15119I: The 'create' action was successful for credential name 'password' of type 'truststore'.

BIP8071I: Successful command completion.

Let's try an report it back to us
C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --report --vault-key someVaultKey --credential-type truststore --credential-name password
BIP15118I: The Integration Server/Integration Node is not running. Only credentials from the 'vault' provider will be shown.
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15121I: The credential name 'password' of type 'truststore' from provider 'servervault' has the following properties defined: 'password', authentication type 'password'.

BIP8071I: Successful command completion.


When creating multiple credentials, for instance userdefined credentials, you can list them all, or just a specific one.
Creating 2
C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --create --vault-key someVaultKey --credential-type userdefined --credential-name ud1 --username matthias --password passw0rd
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15119I: The 'create' action was successful for credential name 'ud1' of type 'userdefined'.

BIP8071I: Successful command completion.

C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --create --vault-key someVaultKey --credential-type userdefined --credential-name ud2 --client-id matthias_client --client-secret passw0rd
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15119I: The 'create' action was successful for credential name 'ud2' of type 'userdefined'.

BIP8071I: Successful command completion.

Reporting all userdefined credentials
C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --report --vault-key someVaultKey --credential-type userdefined
BIP15118I: The Integration Server/Integration Node is not running. Only credentials from the 'vault' provider will be shown.
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15110I: The credential name 'ud1' of type 'userdefined' contains user name 'matthias' from provider 'servervault' and has the following properties defined: 'password', authentication type 'allOptional'.
BIP15121I: The credential name 'ud2' of type 'userdefined' from provider 'servervault' has the following properties defined: 'clientId, clientSecret', authentication type 'allOptional'.

BIP8071I: Successful command completion.

Reporting a specific one
C:\Program Files\IBM\ACE\12.0.12.5>mqsicredentials --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --report --vault-key someVaultKey --credential-type userdefined --credential-name ud2
BIP15118I: The Integration Server/Integration Node is not running. Only credentials from the 'vault' provider will be shown.
BIP15293I: Node or workdir vault key obtained from --vault-key command line argument.
BIP15121I: The credential name 'ud2' of type 'userdefined' from provider 'servervault' has the following properties defined: 'clientId, clientSecret', authentication type 'allOptional'.

BIP8071I: Successful command completion.


Validating inserted credentials
With mqsisetdbparms, you could validate a password by supplying it to the  mqsireportdbparms command 
mqsisetdbparms --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\TEST_SERVER --resource sftp::test --user matthias --passwor
d passw0rd
BIP8071I: Successful command completion.

C:\Program Files\IBM\ACE\12.0.12.5>mqsireportdbparms --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\TEST_SERVER --resource sftp::test --user matthias --passwor passw0rd
BIP8180I: The resource name 'sftp::test' has userID 'matthias'.
BIP8201I: The password you entered, 'passw0rd' for resource 'sftp::test' and userId 'matthias' is correct.
BIP8206I: The Integration node is not running and may not have been restarted since the last change made by the mqsisetdbparms command.

BIP8071I: Successful command completion.


This feature is not available with the mqsicredentials, but you can extract single credentials from the vault using the vault decode feature. The trick of the decode functionality is that you  need to build the path of your credential in the vault, this is credentials/<credentials_type>/<credentials_name>

C:\Program Files\IBM\ACE\12.0.12.5>mqsivault --work-dir C:\Users\Bmatt\IBM\ACET12\workspace\ManageCustomerEnergyService_TEST --vault-key someVaultKey --decode "credentials/userdefined/ud1"
Namespace: credentials
Record: userdefined/ud1
{"name":"ud1","type":"userdefined","properties":{"authType":"allOptional","password":"passw0rd","username":"matthias"}}
BIP8071I: Successful command completion.

Remember this setup, you will need this to prepare you pipeline build!



---
### OVERVIEW

- About SA-dnslookup
- Release notes
- Support and resources

### INSTALLATION

- Hardware and software requirements
- Installation steps 

### USER GUIDE

- Key concepts
- Data types
- Configure SA-dnslookup
- Troubleshooting
- Upgrade
- Copyright & License

---
### OVERVIEW

#### About SA-dnslookup

| Author | Oluwaseun Remi-Omosowon |
| --- | --- |
| App Version | 0.1.0 |
| External components | <ul>SDK for Python 1.7.2</li></ul> |
| Support-addon | This add-on only needs to be installed on the search heads only (Either standalone or dedicated/clustered)|

The SA-dnslookup allows a Splunk® Enterprise user to resolve names or addresses using a custom DNS server
and also specifing a custom DNS search suffix to be used for relative names. The command caches rup to 1000 results.

##### Scripts and binaries

Includes:
- Splunk SDK for Python (1.7.2)
- dnslookup.py : This is the splunk streaming command introduced by this app


#### Release notes

##### About this release

Version 0.1.0 of the SA-dnslookup is compatible with Splunk Enterprise 9.x, 8.x, Splunk Cloud 9.x and Splunk Cloud 9.x.
It will also work with later versions of Splunk that supports Python3. 

| Splunk Enterprise versions | 9.x |
| Splunk Cloud  | 9.x |
| --- | --- |
| CIM | Not Applicable |
| Platforms | Platform independent |
| Lookup file changes | No lookups included in this app |

##### Known issues

There are no known issues in this version.

##### Support and resources

**Questions and answers**

Access questions and answers specific to the SA-dnslookup at (https://answers.splunk.com/).

**Support**

This Splunk support add-on is community supported.

Questions asked on Splunk answers will be answered either by the community of users or by the developer when available.
All support questions should include the version of Splunk and OS.

Issues can also be submitted at the [SA-dnslookup repo via on Github] (https://github.com/seunomosowon/SA-dnslookup/issues)

## INSTALLATION AND CONFIGURATION

### Hardware and software requirements

#### Hardware requirements

SA-dnslookup supports the following server platforms in the versions supported by Splunk Enterprise:

- Linux
- Windows

The app was developed to be platform agnostic, but tests are mostly run on unix.
Please contact the developer with issues running this on Windows.

#### Software requirements

To function properly, SA-dnslookup has no external requirements but needs to be installed on a full Splunk install
which provides python3.


#### Splunk Enterprise system requirements

Because this add-on runs on Splunk Enterprise, all of the [Splunk Enterprise system requirements](http://docs.splunk.com/Documentation/Splunk/latest/Installation/Systemrequirements) apply.

#### Download

Download the SA-dnslookup at [GitHub](https://github.com/seunomosowon/SA-geodistance).

#### Installation steps

To install and configure this app on your supported standalone platform, do one of the following:

- Install on a standalone search head via the GUI (https://docs.splunk.com/Documentation/AddOns/released/Overview/Singleserverinstall)
- Extract the app to ```$SPLUNK_HOME/etc/apps/``` and restart Splunk

For a supported distributed environment, follow the steps to install the SA-geodistance on the search head only.

For a clustered search head environment, install SA-geodistance via the search head deployer.

More instructions available at the following [URL] (https://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall)

For Splunk cloud installations, follow the instructions present at the following [link] (https://docs.splunk.com/Documentation/AddOns/released/Overview/SplunkCloudinstall)


## USER GUIDE

### Key concepts for SA-dnslookup

<code>
<base_search> dnslookup (recordtype=<string>) (input_field=<string>) | (output_field=<string>) | 
                  (search_suffix=<string>)? | (server=<string>)*
</code>

This app looks up the value of the field passed in `input_field`, and saves the response to `output_field`
using either the system resolver or any custom resolver passed as a list of servers.
This command can also take a list of search_suffixes to be used to search for hostnames.

Record types requested can include any of the DNS record types or FORWARD / REVERSE which corresponds to 
A and PTR respectively

#### Example

```
| makeresults 
| eval _raw = "www.google.com,4.2.2.2", shost="encrypted"
| rex "^(?<h>[\w\.\-]+),(?<ip>.*)$"
| dnslookup recordtype="FORWARD" input_field=h output_field="dst_ip"  search_suffix="google.com,yahoo.com" server=8.8.8.8,8.8.4.4
| dnslookup recordtype="ptr" input_field=ip output_field="dest_host"  search_suffix="google.com,yahoo.com"
| dnslookup recordtype="AAAA" input_field=shost output_field="dst_ip6"  search_suffix="google.com"
```

Scenario 1:
``` 
| dnslookup recordtype="FORWARD" input_field=h output_field="dst_ip"  search_suffix="google.com,yahoo.com" server=8.8.8.8,8.8.4.4 
```

This tries to resolve the name www.google.com using the custom dns servers provided. It resolves the names without the suffices 
since the name is a fully qualified domain name. The output is stored in dst_ip.

Scenario 2:
``` 
| dnslookup recordtype="ptr" input_field=ip output_field="dest_host"  search_suffix="google.com,yahoo.com"
```

This tries to resolve the IP: 4.2.2.2 to the dest_host.  

Scenario 3:
``` 
| dnslookup recordtype="AAAA" input_field=shost output_field="dst_ip6"  search_suffix="google.com"
```

This command resolves the the relative name "encrypted" using the DNS suffix "google.com" into the IPv6 address.
and writes the output to dst_ip6.


### Data types

This app outputs the DNS resolution result to the output_field parameter.


### Configure SA-dnslookup

This app has no configurations.


### Upgrade SA-geodistance
This app supports in-place upgrade of older verisons. Alternatively, remove older versions before installing the newest version.


### Copyright & License

#### Copyright - Splunk SDK for Python

The Splunk SDK for Python is licensed under the Apache License 2.0 which can be found at: (https://www.apache.org/licenses/LICENSE-2.0)


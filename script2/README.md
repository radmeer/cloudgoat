# AWS exploits SAGA

## (SCRIPT2) Neo's Proxy: Breaking the Matrix Inside Out

In the vast expanse of the Matrix, Neo, finds himself an outsider - a zero in a world of ones. Unseen and unnoticed, he's just an anonymous fragment in the infinite realm of data. Yet, Neo is no ordinary fragment. In his code flows the audacity to challenge the established order, an aspiration to breach the impenetrable fortress of privilege. A misconfigured sentinel, a reverse-proxy server, presents Neo with the opportunity he seeks.

Much like a keymaker, Neo crafts his entry. He queries the EC2 metadata service, an unassuming gatekeeper of secrets, to acquire the 'instance profile keys' the digital equivalent of the Matrix's backdoors. 

In the blink of an eye, the faceless Neo morphs into an entity of significance, armed with newfound privileges that even Agent Smith would take notice of. With the keys in his possession, Neo traverses the labyrinthine Matrix, bypassing security checks as if he'd known the code his entire life.

As he delves deeper into the Matrix, he finds what he seeks - the sensitive data within the S3 bucket. His mission culminates in the successful exfiltration of the coveted information, proving yet again that in the Matrix, even an outsider can defy the rules.

## Summary

Starting as an anonymous outsider with no access or privileges, exploit a misconfigured reverse-proxy server to query the EC2 metadata service and acquire instance profile keys. Then, use those keys to discover, access, and exfiltrate sensitive data from an S3 bucket.

## Scenario Start(s)

1. The IP Address of an EC2 server is running a misconfigured reverse proxy
2. Player name and credentials to access lambda
3. lambda function name to invoke with secret payload

## Scenario Goal(s)

Download the confidential files from the S3 bucket

## Exploitation Route(s)

![Scenario Route(s)](https://www.lucidchart.com/publicSegments/view/3ffe907e-6281-47e9-b7bf-e07fdcb48103/image.png)

## Route Walkthrough - Anonymous Attacker

1. The attacker finds the IP of an EC2 instance by shady means, and after some reconnaissance realizes that it is acting as a reverse-proxy server. This is common, especially for organizations in the process of moving from on-premise to the cloud.
2. After some research, the attacker uses `CURL` to send a request to the web server and set the host header to the IP address of EC2 metadata service.
3. The attacker's specially-crafted CURL command is successful, returning the Access Key ID, Secret Access Key, and Session Token of the IAM Instance Profile attached to the EC2 instance.
4. With the IAM role's credentials in hand, the attacker is now able to explore the victim's cloud environment using the powerful permissions granted to the role.
5. The attacker is then able to list, identify, and access a private S3 bucket.
6. Inside the private S3 bucket, the attacker finds several files full of sensitive information, and is able to download these to their local machine for dissemination.
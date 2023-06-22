# AWS exploits SAGA

## Harry Potter and the Chamber of Privileges (SCRIPT1)

From a place of extremely constrained privileges, Harry, found himself within the complex and arcane world of IAM policy versions. Buried within these digital layers of time, there lay dormant older policies, forgotten relics of an era less secure, that granted privileges of an alarmingly unrestricted nature.

With carefully constructed arcane cli spell , Harry restored one such relic. Much like the act of unlocking the Chamber of Secrets itself, this allowed him an unparalleled escalation of his powers. No longer was he merely an observer within the digital corridors of the institution. Just as the Chamber of Secrets held a powerful creature within its depths, the policy versions held a force of comparable magnitude. 

## Summary

Starting with a highly-limited IAM user, Harry is able to review previous IAM policy versions and restore one which allows full admin privileges, resulting in a privilege escalation exploit and entrance to secret Horwarts chambers.

## Exploitation Route(s)

![Scenario Route(s)](https://www.lucidchart.com/publicSegments/view/acef779c-51ce-4582-b4d2-19ae92b7f170/image.png)

## Route Walkthrough - IAM User "hogwarts_user"

1. Starting as the IAM user "hogwarts_user," the attacker has only a few limited - seemingly harmless - privileges available to them.
2. The attacker analyzes hogwarts_user's privileges and notices the SetDefaultPolicyVersion permission - allowing access to 4 other versions of the policy via setting an old version as the default.
3. After reviewing the old policy versions, the attacker finds that one version in particular offers a full set of admin rights.
4. Attacker restores the full-admin policy version, gaining full admin privileges and the ability to carry out any malicious actions they wish.
5. As a final step, the attacker may choose to revert hogwarts_user's policy version back to the original one, thereby concealing their actions and the true capabilities of the IAM user.
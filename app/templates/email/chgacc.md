Hi, {{name}}
==============
You have changed your profile.  
Make sure that is changed by yourself or you can email  
**jeefy** (jeefy163@163.com) or **Fu Weiji** (2925581093@qq.com)  
However, make sure that your password is safe enough or change your password to a stronger password immediately.

- - -
Account Now
--------------
_Name_: {{user.name}}  
___Email: {{user.email}}___  
_full name_: {{user.full_name}}  
_Permission_: {{user.per}}  
_description_:
{% for line in user.linedes %}  
{{line}}  
{% endfor %}  
_country_: {{user.pl}}

- - -
For change the profile image, please get to [gravatar.com](https://gravatar.com) to change your profile image.  
Notice that your signing in email at gravatar must match the account at Jeefy, or the image would not show.

- - -
# image now
![Profile image]({{user.gravatar}})
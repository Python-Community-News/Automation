## Topics
{% for issue in issue.get_content_issues('issues') %}
### {{issue.title}}

<small>Submitted by: [{{issue._user.login}}]({{issue._user.url}}) on {{issue._created_at|datetime_format}}</small>

{{issue.summary}}
{% endfor %}

### Conferences

{% for conf in issue.get_content_issues('conferences') %}
* [{{conf.conference_name}}]({{conf.url}})
{% endfor %}


### Watch the VOD on Youtube:
https://youtube.com/watch/{{issue.youtube}}

### Take the content on the road with you!
https://share.transistor.fm/s/{{issue.podcast}}

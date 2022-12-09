## Main Topics
{% for topic in issue.get_content_issues('issues') %}
### {{topic.title}}

<small>Submitted by: [{{topic._user.login}}]({{topic._user.url}}) on {{topic._created_at|datetime_format}}</small>

{{topic.summary}}
{% endfor %}

You can share your thoughts on this topic by watching this week's Python Community News Extra!

https://youtube.com/watch/{{issue.youtube}}

### Around the Community

Get news from the community by subscribing to our [YouTube Channel](youtube.com/@pycommunitynews).

{% for topic in issue.get_content_issues('shorts') %}
### {{topic.title}}

<small>Submitted by: [{{topic._user.login}}]({{topic._user.url}}) on {{topic._created_at|datetime_format}}</small>

https://youtube.com/watch/{{topic.youtube}}

{{topic.summary}}
{% endfor %}


### Conferences

{% for conf in issue.get_content_issues('conferences') %}
* [{{conf.title}}]({{conf.url}})

{% if conf['summary'] %}
    {{conf.summary}}
{% endif %}

{% endfor %}


Catch up on the podcast and past issues at <https://pythoncommunitynews.com>
